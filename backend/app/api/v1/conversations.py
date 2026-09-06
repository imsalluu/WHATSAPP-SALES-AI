from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.deps import get_current_organization, get_current_user
from app.models.organization import Organization
from app.models.user import User
from app.models.customer import Customer
from app.models.conversation import Conversation, Message, ConversationStatus, SenderType
from app.schemas.conversation import (
    ConversationOut,
    ConversationDetailOut,
    MessageOut,
    SendMessageRequest,
    SimulatorMessageRequest,
    SimulatorResponse,
)
from app.agents.sales_agent import SalesAgent

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get("/", response_model=List[ConversationOut])
async def list_conversations(
    status_filter: Optional[str] = None,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Conversation, Customer).join(Customer, Conversation.customer_id == Customer.id).where(
        Conversation.organization_id == current_org.id
    )
    if status_filter:
        stmt = stmt.where(Conversation.status == status_filter.upper())
    stmt = stmt.order_by(desc(Conversation.last_message_at))

    result = await db.execute(stmt)
    rows = result.all()

    conversations_out = []
    for conv, cust in rows:
        conv.customer = cust
        # Fetch last message
        last_m_stmt = select(Message).where(Message.conversation_id == conv.id).order_by(desc(Message.created_at)).limit(1)
        last_m_res = await db.execute(last_m_stmt)
        conv.last_message = last_m_res.scalars().first()
        conversations_out.append(conv)

    return conversations_out


@router.get("/{conversation_id}", response_model=ConversationDetailOut)
async def get_conversation(
    conversation_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Conversation, Customer).join(Customer, Conversation.customer_id == Customer.id).where(
        Conversation.id == conversation_id,
        Conversation.organization_id == current_org.id,
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv, cust = row
    conv.customer = cust

    msgs_stmt = select(Message).where(
        Message.conversation_id == conv.id,
        Message.organization_id == current_org.id,
    ).order_by(Message.created_at.asc())
    msgs_res = await db.execute(msgs_stmt)
    conv.messages = msgs_res.scalars().all()

    return conv


@router.post("/{conversation_id}/takeover")
async def takeover_conversation(
    conversation_id: str,
    current_org: Organization = Depends(get_current_organization),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Human agent takes over live conversation, pausing AI responses."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.organization_id == current_org.id,
    )
    res = await db.execute(stmt)
    conv = res.scalars().first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv.status = ConversationStatus.HUMAN_ACTIVE.value

    # Add system notification message
    sys_msg = Message(
        organization_id=current_org.id,
        conversation_id=conv.id,
        sender_type=SenderType.SYSTEM.value,
        content=f"Human Agent {current_user.full_name} joined the chat. AI responses paused.",
    )
    db.add(sys_msg)
    await db.commit()
    return {"message": "Successfully took over conversation", "status": conv.status}


@router.post("/{conversation_id}/release")
async def release_conversation(
    conversation_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """Releases conversation back to AI Sales Agent."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.organization_id == current_org.id,
    )
    res = await db.execute(stmt)
    conv = res.scalars().first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv.status = ConversationStatus.AI_ACTIVE.value

    sys_msg = Message(
        organization_id=current_org.id,
        conversation_id=conv.id,
        sender_type=SenderType.SYSTEM.value,
        content="Conversation released back to AI Sales Agent.",
    )
    db.add(sys_msg)
    await db.commit()
    return {"message": "Conversation released to AI", "status": conv.status}


@router.post("/{conversation_id}/messages", response_model=MessageOut)
async def send_human_agent_message(
    conversation_id: str,
    data: SendMessageRequest,
    current_org: Organization = Depends(get_current_organization),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Sends a live message from a human agent to the customer."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.organization_id == current_org.id,
    )
    res = await db.execute(stmt)
    conv = res.scalars().first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    msg = Message(
        organization_id=current_org.id,
        conversation_id=conv.id,
        sender_type=SenderType.HUMAN_AGENT.value,
        sender_id=current_user.id,
        content=data.content,
        media_url=data.media_url,
        media_type=data.media_type,
    )
    db.add(msg)
    conv.last_message_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(msg)
    return msg


@router.post("/simulator", response_model=SimulatorResponse)
async def run_simulator_message(
    req: SimulatorMessageRequest,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """
    In-Browser WhatsApp Simulator:
    Simulates a live inbound customer message from WhatsApp, triggers the AI agent,
    and returns tool execution steps and AI response.
    """
    # 1. Find or create customer
    cust_stmt = select(Customer).where(
        Customer.organization_id == current_org.id,
        Customer.phone_number == req.phone_number,
    )
    c_res = await db.execute(cust_stmt)
    customer = c_res.scalars().first()

    if not customer:
        customer = Customer(
            organization_id=current_org.id,
            phone_number=req.phone_number,
            name=req.customer_name or "WhatsApp Visitor",
        )
        db.add(customer)
        await db.flush()

    # 2. Find or create conversation
    conv_stmt = select(Conversation).where(
        Conversation.organization_id == current_org.id,
        Conversation.customer_id == customer.id,
    ).order_by(desc(Conversation.last_message_at))
    conv_res = await db.execute(conv_stmt)
    conversation = conv_res.scalars().first()

    if not conversation:
        conversation = Conversation(
            organization_id=current_org.id,
            customer_id=customer.id,
            status=ConversationStatus.AI_ACTIVE.value,
        )
        db.add(conversation)
        await db.flush()

    # 3. Add Customer Message
    cust_msg = Message(
        organization_id=current_org.id,
        conversation_id=conversation.id,
        sender_type=SenderType.CUSTOMER.value,
        content=req.message,
    )
    db.add(cust_msg)
    conversation.last_message_at = datetime.now(timezone.utc)
    await db.flush()

    # 4. If AI is ACTIVE, run AI Sales Agent
    ai_response_msg = None
    tools_executed = []

    if conversation.status == ConversationStatus.AI_ACTIVE.value:
        agent = SalesAgent(db=db, organization_id=current_org.id)
        agent_result = await agent.process_message(
            conversation=conversation,
            customer=customer,
            incoming_message_text=req.message,
        )
        ai_response_msg = agent_result["message_obj"]
        tools_executed = agent_result["tools_executed"]

    await db.commit()
    await db.refresh(cust_msg)
    if ai_response_msg:
        await db.refresh(ai_response_msg)

    return SimulatorResponse(
        conversation_id=conversation.id,
        status=conversation.status,
        customer_message=cust_msg,
        ai_response=ai_response_msg,
        tools_executed=tools_executed,
        buying_stage=conversation.buying_stage,
        cart_state=conversation.cart_state or {},
    )
