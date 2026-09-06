from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.schemas.customer import CustomerOut


class MessageOut(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    sender_id: Optional[str] = None
    content: str
    tool_calls: List[Dict[str, Any]] = []
    tool_results: List[Dict[str, Any]] = []
    whatsapp_message_id: Optional[str] = None
    status: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    id: str
    organization_id: str
    customer_id: str
    status: str
    buying_stage: str
    current_intent: str
    cart_state: Dict[str, Any] = {}
    pending_order_data: Dict[str, Any] = {}
    summary: Optional[str] = None
    last_message_at: datetime
    created_at: datetime
    customer: Optional[CustomerOut] = None
    last_message: Optional[MessageOut] = None

    class Config:
        from_attributes = True


class ConversationDetailOut(ConversationOut):
    messages: List[MessageOut] = []


class SendMessageRequest(BaseModel):
    content: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None


class SimulatorMessageRequest(BaseModel):
    phone_number: str
    customer_name: Optional[str] = "Walk-in WhatsApp Buyer"
    message: str


class SimulatorResponse(BaseModel):
    conversation_id: str
    status: str
    customer_message: MessageOut
    ai_response: Optional[MessageOut] = None
    tools_executed: List[Dict[str, Any]] = []
    buying_stage: str
    cart_state: Dict[str, Any] = {}
