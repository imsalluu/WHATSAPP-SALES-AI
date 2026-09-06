from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class WhatsAppProvider(ABC):
    @abstractmethod
    async def send_message(self, recipient_phone: str, message: str, preview_url: bool = False) -> Dict[str, Any]:
        """Sends standard text message."""
        pass

    @abstractmethod
    async def send_template(self, recipient_phone: str, template_name: str, language_code: str = "en", components: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Sends approved Meta WhatsApp template."""
        pass

    @abstractmethod
    async def send_interactive_buttons(self, recipient_phone: str, body_text: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """Sends quick reply interactive buttons."""
        pass

    @abstractmethod
    async def mark_read(self, message_id: str) -> bool:
        """Marks incoming WhatsApp message as read."""
        pass
