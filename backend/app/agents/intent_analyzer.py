import re
from typing import Dict, Any, Tuple


class IntentAnalyzer:
    @staticmethod
    def analyze(message: str, conversation_context: Dict[str, Any] = None) -> Tuple[str, str, int]:
        """
        Analyzes message content to determine:
        1. Primary intent
        2. Buying stage (AWARENESS, CONSIDERATION, DECISION, RETENTION)
        3. Lead score (0 to 100)
        """
        msg = message.lower().strip()
        context = conversation_context or {}
        pending_order = context.get("pending_order_data", {})

        # 1. Human Handoff Triggers
        human_triggers = ["human", "agent", "person", "representative", "manager", "support", "talk to human", "manush", "kotha bolbo", "live chat"]
        if any(trigger in msg for trigger in human_triggers):
            return "HUMAN_HANDOFF", "DECISION", 40

        # 2. Order Confirmation (if pending order exists)
        confirm_words = ["yes", "confirm", "order", "place", "sure", "proceed", "hha", "thik ache", "ok", "done", "plz confirm", "order koren"]
        if pending_order and any(w == msg or w in msg.split() for w in confirm_words):
            return "ORDER_CONFIRMATION", "DECISION", 95

        # 3. Order Tracking
        tracking_triggers = ["track", "status", "where is my order", "order number", "ord-", "delivery status", "kothay ache", "tracking"]
        if any(tr in msg for tr in tracking_triggers) or re.search(r"ord-\d+", msg):
            return "ORDER_TRACKING", "RETENTION", 80

        # 4. Inventory / Size / Color Check
        inventory_triggers = ["available", "in stock", "stock", "size", "color", "xl", "xxl", "large", "medium", "small", "ache kina", "available ache"]
        if any(it in msg for it in inventory_triggers):
            return "INVENTORY_CHECK", "CONSIDERATION", 75

        # 5. Order Creation / Purchase Intent
        purchase_triggers = ["buy", "order", "purchase", "kenbo", "nite chai", "order korte chai", "address", "cash on delivery", "cod", "bkash"]
        if any(pt in msg for pt in purchase_triggers) or re.search(r"01\d{9}", msg):  # Phone number detected
            return "ORDER_CREATION", "DECISION", 90

        # 6. Shipping / Delivery Inquiry
        shipping_triggers = ["shipping", "delivery", "charge", "courier", "cost", "koto taka delivery", "kobe pabo", "how many days"]
        if any(st in msg for st in shipping_triggers):
            return "SHIPPING_INQUIRY", "CONSIDERATION", 65

        # 7. Price / Discount Inquiry
        price_triggers = ["price", "cost", "dam", "koto", "discount", "offer", "budget", "taka", "৳"]
        if any(pt in msg for pt in price_triggers):
            return "PRICE_INQUIRY", "CONSIDERATION", 70

        # 8. Product Search / Gift Discovery
        search_triggers = ["looking for", "need", "show me", "gift", "collection", "product", "hoodie", "shirt", "t-shirt", "watch", "shoe", "dress", "dekhan"]
        if any(st in msg for st in search_triggers):
            return "PRODUCT_SEARCH", "AWARENESS", 60

        # 9. Objection Handling
        objection_triggers = ["expensive", "too high", "dam beshi", "quality", "original", "fake", "guarantee", "warranty", "return kora jabe"]
        if any(ot in msg for ot in objection_triggers):
            return "OBJECTION_HANDLING", "CONSIDERATION", 65

        # 10. Greeting
        greeting_triggers = ["hi", "hello", "hey", "salam", "assalamu alaikum", "namaskar", "good morning", "good evening"]
        if any(gt == msg or msg.startswith(gt) for gt in greeting_triggers):
            return "GREETING", "AWARENESS", 40

        return "GENERAL_INQUIRY", "AWARENESS", 50
