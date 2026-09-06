from sqlalchemy import Column, String, Float, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
import enum
from app.models.base import TenantModel


class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    CONVERTED = "CONVERTED"
    LOST = "LOST"


class Lead(TenantModel):
    __tablename__ = "leads"

    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=True)
    phone = Column(String(50), index=True, nullable=False)
    intent = Column(String(255), nullable=True)
    interested_products = Column(JSON, default=list, nullable=False)
    budget = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)
    lead_score = Column(Integer, default=50, nullable=False)  # 0 to 100
    status = Column(String(50), default=LeadStatus.NEW.value, nullable=False, index=True)
    objections = Column(JSON, default=list, nullable=False)
    notes = Column(String(1024), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="leads")
