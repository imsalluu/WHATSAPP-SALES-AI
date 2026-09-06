from sqlalchemy import Column, String, Boolean, JSON
import enum
from app.models.base import TenantModel


class WhatsAppStatus(str, enum.Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"


class WhatsAppAccount(TenantModel):
    __tablename__ = "whatsapp_accounts"

    phone_number_id = Column(String(100), nullable=True)
    waba_id = Column(String(100), nullable=True)  # WhatsApp Business Account ID
    display_phone_number = Column(String(50), nullable=True)
    verified_name = Column(String(255), nullable=True)
    
    access_token = Column(String(1024), nullable=True)
    webhook_verify_token = Column(String(255), nullable=False, default="sales_ai_webhook_verify_secret")
    
    status = Column(String(50), default=WhatsAppStatus.CONNECTED.value, nullable=False)
    is_live_enabled = Column(Boolean, default=True, nullable=False)
    account_metadata = Column(JSON, default=dict, nullable=False)
