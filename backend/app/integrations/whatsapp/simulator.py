import uuid
from typing import Dict, Any, Optional, List
from app.integrations.whatsapp.provider import WhatsAppProvider


class SimulatorWhatsAppProvider(WhatsAppProvider):
    """
    Mock & In-Browser Simulator Provider for frictionless development, testing,
    and demoing sales flows without requiring live Meta Business developer accounts.
    """
    def __init__(self):
        self.sent_messages: List[Dict[str, Any]] = []

    async def send_message(self, recipient_phone: str, message: str, preview_url: bool = False) -> Dict[str, Any]:
        msg_id = f"sim_msg_{uuid.uuid4().hex[:12]}"
        record = {
            "messaging_product": "whatsapp",
            "contacts": [{"input": recipient_phone, "wa_id": recipient_phone}],
            "messages": [{"id": msg_id}],
            "_simulated": True,
            "_body": message,
        }
        self.sent_messages.append(record)
        return record

    async def send_template(self, recipient_phone: str, template_name: str, language_code: str = "en", components: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        msg_id = f"sim_tpl_{uuid.uuid4().hex[:12]}"
        return {
            "messaging_product": "whatsapp",
            "contacts": [{"input": recipient_phone, "wa_id": recipient_phone}],
            "messages": [{"id": msg_id}],
            "_simulated": True,
            "_template": template_name,
        }

    async def send_interactive_buttons(self, recipient_phone: str, body_text: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        msg_id = f"sim_btn_{uuid.uuid4().hex[:12]}"
        return {
            "messaging_product": "whatsapp",
            "contacts": [{"input": recipient_phone, "wa_id": recipient_phone}],
            "messages": [{"id": msg_id}],
            "_simulated": True,
            "_buttons": buttons,
        }

    async def mark_read(self, message_id: str) -> bool:
        return True
