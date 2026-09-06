from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base import TenantModel, get_utc_now


class ConversationStatus(str, enum.Enum):
    AI_ACTIVE = "AI_ACTIVE"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"
    HUMAN_ACTIVE = "HUMAN_ACTIVE"
    RESOLVED = "RESOLVED"


class BuyingStage(str, enum.Enum):
    AWARENESS = "AWARENESS"
    CONSIDERATION = "CONSIDERATION"
    DECISION = "DECISION"
    RETENTION = "RETENTION"


class SenderType(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    AI = "AI"
    HUMAN_AGENT = "HUMAN_AGENT"
    SYSTEM = "SYSTEM"


class MessageStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    FAILED = "FAILED"


class Conversation(TenantModel):
    __tablename__ = "conversations"

    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default=ConversationStatus.AI_ACTIVE.value, nullable=False, index=True)
    buying_stage = Column(String(50), default=BuyingStage.AWARENESS.value, nullable=False)
    current_intent = Column(String(100), default="GENERAL_INQUIRY", nullable=False)
    
    # Active shopping context & pending confirmation
    cart_state = Column(JSON, default=dict, nullable=False)
    pending_order_data = Column(JSON, default=dict, nullable=False)
    
    summary = Column(Text, nullable=True)
    last_message_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    orders = relationship("Order", back_populates="conversation")


class Message(TenantModel):
    __tablename__ = "messages"

    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_type = Column(String(50), default=SenderType.CUSTOMER.value, nullable=False)
    sender_id = Column(String(36), nullable=True)
    content = Column(Text, nullable=False)
    
    tool_calls = Column(JSON, default=list, nullable=False)
    tool_results = Column(JSON, default=list, nullable=False)
    
    whatsapp_message_id = Column(String(255), unique=True, index=True, nullable=True)
    status = Column(String(50), default=MessageStatus.SENT.value, nullable=False)
    media_url = Column(String(1024), nullable=True)
    media_type = Column(String(50), nullable=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
