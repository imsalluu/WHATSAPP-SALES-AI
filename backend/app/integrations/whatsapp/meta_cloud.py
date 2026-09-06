import httpx
from typing import Dict, Any, Optional, List
from app.integrations.whatsapp.provider import WhatsAppProvider
from app.core.config import settings


class MetaWhatsAppCloudProvider(WhatsAppProvider):
    def __init__(self, phone_number_id: str, access_token: str):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.base_url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_API_VERSION}/{phone_number_id}"

    async def send_message(self, recipient_phone: str, message: str, preview_url: bool = False) -> Dict[str, Any]:
        """Sends a text message using Meta WhatsApp Cloud API."""
        clean_phone = recipient_phone.replace("+", "").replace("-", "").replace(" ", "")
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_phone,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message,
            }
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
            return resp.json()

    async def send_template(self, recipient_phone: str, template_name: str, language_code: str = "en", components: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Sends an approved WhatsApp template."""
        clean_phone = recipient_phone.replace("+", "").replace("-", "").replace(" ", "")
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": components or []
            }
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
            return resp.json()

    async def send_interactive_buttons(self, recipient_phone: str, body_text: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """Sends interactive action buttons."""
        clean_phone = recipient_phone.replace("+", "").replace("-", "").replace(" ", "")
        action_buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": b.get("id", f"btn_{i}"),
                    "title": b.get("title", "Select")[:20]
                }
            }
            for i, b in enumerate(buttons[:3])  # Max 3 buttons in WhatsApp API
        ]
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": action_buttons}
            }
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
            return resp.json()

    async def mark_read(self, message_id: str) -> bool:
        """Marks message as read."""
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
                return resp.status_code == 200
        except Exception:
            return False
