from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.config import settings
from app.core.security import verify_whatsapp_signature
from app.core.deps import get_current_organization, require_roles
from app.models.organization import Organization, RoleType
from app.models.whatsapp_account import WhatsAppAccount, WhatsAppStatus
from app.models.customer import Customer
from app.models.conversation import Conversation, Message, ConversationStatus, SenderType
from app.schemas.whatsapp import WhatsAppConnectRequest, WhatsAppAccountOut, SendTestMessageRequest
from app.integrations.whatsapp.meta_cloud import MetaWhatsAppCloudProvider
from app.agents.sales_agent import SalesAgent
from datetime import datetime, timezone

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Integration"])


@router.get("/webhook")
async def verify_webhook(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta WhatsApp Cloud API Webhook Verification Endpoint."""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_DEFAULT_VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/webhook")
async def handle_whatsapp_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    db: AsyncSession = Depends(get_db),
):
    """
    Handles live incoming WhatsApp webhook events from Meta Cloud API.
    Verifies HMAC signature, extracts messages, and dispatches to AI Sales Agent.
    """
    body_bytes = await request.body()
    # Verify HMAC signature
    is_valid = verify_whatsapp_signature(body_bytes, x_hub_signature_256, settings.WHATSAPP_APP_SECRET)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid webhook signature")

    payload = await request.json()
    entries = payload.get("entry", [])

    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])
            metadata = value.get("metadata", {})
            phone_number_id = metadata.get("phone_number_id")

            # Lookup WhatsApp account by phone_number_id
            wa_stmt = select(WhatsAppAccount).where(WhatsAppAccount.phone_number_id == phone_number_id)
            wa_res = await db.execute(wa_stmt)
            wa_account = wa_res.scalars().first()

            if not wa_account:
                # Fallback to first active organization in database if phone_number_id not registered
                wa_fallback_stmt = select(WhatsAppAccount).limit(1)
                wa_res = await db.execute(wa_fallback_stmt)
                wa_account = wa_res.scalars().first()

            if not wa_account:
                continue

            org_id = wa_account.organization_id

            for msg_item in messages:
                wa_msg_id = msg_item.get("id")
                sender_phone = msg_item.get("from")
                msg_type = msg_item.get("type")
                
                msg_text = ""
                if msg_type == "text":
                    msg_text = msg_item.get("text", {}).get("body", "")
                elif msg_type == "interactive":
                    btn_reply = msg_item.get("interactive", {}).get("button_reply", {})
                    msg_text = btn_reply.get("title", "")
                
                if not msg_text:
                    continue

                # Deduplicate message by wa_msg_id
                dup_stmt = select(Message).where(Message.whatsapp_message_id == wa_msg_id)
                dup_res = await db.execute(dup_stmt)
                if dup_res.scalar_one_or_none():
                    continue

                # 1. Customer
                c_stmt = select(Customer).where(Customer.organization_id == org_id, Customer.phone_number == sender_phone)
                c_res = await db.execute(c_stmt)
                customer = c_res.scalars().first()
                if not customer:
                    customer = Customer(organization_id=org_id, phone_number=sender_phone)
                    db.add(customer)
                    await db.flush()

                # 2. Conversation
                conv_stmt = select(Conversation).where(
                    Conversation.organization_id == org_id,
                    Conversation.customer_id == customer.id,
                ).order_by(Conversation.last_message_at.desc())
                conv_res = await db.execute(conv_stmt)
                conversation = conv_res.scalars().first()
                if not conversation:
                    conversation = Conversation(
                        organization_id=org_id,
                        customer_id=customer.id,
                        status=ConversationStatus.AI_ACTIVE.value,
                    )
                    db.add(conversation)
                    await db.flush()

                # 3. Add Customer Message
                c_msg = Message(
                    organization_id=org_id,
                    conversation_id=conversation.id,
                    sender_type=SenderType.CUSTOMER.value,
                    content=msg_text,
                    whatsapp_message_id=wa_msg_id,
                )
                db.add(c_msg)
                conversation.last_message_at = datetime.now(timezone.utc)
                await db.flush()

                # 4. Run AI Agent if active
                if conversation.status == ConversationStatus.AI_ACTIVE.value:
                    agent = SalesAgent(db=db, organization_id=org_id)
                    agent_res = await agent.process_message(
                        conversation=conversation,
                        customer=customer,
                        incoming_message_text=msg_text,
                    )
                    
                    # Send response back via WhatsApp Cloud API if credentials set
                    if wa_account.access_token and wa_account.phone_number_id:
                        provider = MetaWhatsAppCloudProvider(
                            phone_number_id=wa_account.phone_number_id,
                            access_token=wa_account.access_token,
                        )
                        await provider.send_message(
                            recipient_phone=sender_phone,
                            message=agent_res["response"],
                        )

                await db.commit()

    return {"status": "success"}


@router.get("/account", response_model=WhatsAppAccountOut)
async def get_whatsapp_account(
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(WhatsAppAccount).where(WhatsAppAccount.organization_id == current_org.id)
    res = await db.execute(stmt)
    account = res.scalars().first()
    if not account:
        account = WhatsAppAccount(
            organization_id=current_org.id,
            webhook_verify_token="sales_ai_webhook_verify_secret",
            status=WhatsAppStatus.CONNECTED.value,
            display_phone_number="+880 1800-SALESAI",
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
    return account


@router.post("/connect", response_model=WhatsAppAccountOut)
async def connect_whatsapp_account(
    data: WhatsAppConnectRequest,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value])),
):
    stmt = select(WhatsAppAccount).where(WhatsAppAccount.organization_id == current_org.id)
    res = await db.execute(stmt)
    account = res.scalars().first()
    if not account:
        account = WhatsAppAccount(organization_id=current_org.id)
        db.add(account)

    account.phone_number_id = data.phone_number_id
    account.waba_id = data.waba_id
    account.display_phone_number = data.display_phone_number
    account.access_token = data.access_token
    if data.webhook_verify_token:
        account.webhook_verify_token = data.webhook_verify_token
    account.status = WhatsAppStatus.CONNECTED.value

    await db.commit()
    await db.refresh(account)
    return account


@router.post("/test-message")
async def send_test_message(
    req: SendTestMessageRequest,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    """Sends a test WhatsApp message to verify phone connectivity."""
    stmt = select(WhatsAppAccount).where(WhatsAppAccount.organization_id == current_org.id)
    res = await db.execute(stmt)
    account = res.scalars().first()

    if account and account.access_token and account.phone_number_id:
        provider = MetaWhatsAppCloudProvider(
            phone_number_id=account.phone_number_id,
            access_token=account.access_token,
        )
        send_res = await provider.send_message(recipient_phone=req.recipient_phone, message=req.message)
        return {"status": "sent", "provider": "Meta WhatsApp Cloud API", "meta_response": send_res}

    return {
        "status": "simulated",
        "provider": "Simulator",
        "recipient": req.recipient_phone,
        "message": req.message,
        "note": "Connect live Meta access token in Settings to deliver over real cellular network."
    }
