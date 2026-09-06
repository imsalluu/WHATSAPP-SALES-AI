from sqlalchemy import Column, String, JSON
from app.models.base import TenantModel


class AuditLog(TenantModel):
    __tablename__ = "audit_logs"

    actor_type = Column(String(50), default="USER", nullable=False)  # USER, AI, SYSTEM, WEBHOOK
    actor_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)  # e.g., "ORDER_CREATED", "AGENT_TAKEOVER", "PRODUCT_UPDATED"
    entity_type = Column(String(50), nullable=False)  # "ORDER", "CONVERSATION", "PRODUCT", "LEAD"
    entity_id = Column(String(36), nullable=True)
    details = Column(JSON, default=dict, nullable=False)
