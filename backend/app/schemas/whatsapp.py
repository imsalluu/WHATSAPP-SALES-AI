from typing import Optional, Dict, Any
from pydantic import BaseModel


class WhatsAppConnectRequest(BaseModel):
    phone_number_id: str
    waba_id: str
    display_phone_number: str
    access_token: str
    webhook_verify_token: Optional[str] = "sales_ai_webhook_verify_secret"


class WhatsAppAccountOut(BaseModel):
    id: str
    organization_id: str
    phone_number_id: Optional[str] = None
    waba_id: Optional[str] = None
    display_phone_number: Optional[str] = None
    verified_name: Optional[str] = None
    webhook_verify_token: str
    status: str
    is_live_enabled: bool

    class Config:
        from_attributes = True


class SendTestMessageRequest(BaseModel):
    recipient_phone: str
    message: str
