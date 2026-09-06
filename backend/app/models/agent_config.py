from sqlalchemy import Column, String, JSON, Text, Boolean
from app.models.base import TenantModel


class AgentConfig(TenantModel):
    __tablename__ = "agent_configs"

    agent_name = Column(String(100), default="Sales Copilot", nullable=False)
    personality = Column(String(100), default="Friendly, consultative and concise", nullable=False)
    tone = Column(String(50), default="Professional & Helpful", nullable=False)
    language = Column(String(50), default="English / Bengali (Banglish)", nullable=False)
    greeting_message = Column(Text, default="Hello! Welcome to our store. How can I help you today?", nullable=False)
    
    custom_system_prompt = Column(Text, nullable=True)
    sales_instructions = Column(Text, nullable=True)
    
    # Store/Business policies overview in prompt
    business_description = Column(Text, nullable=True)
    shipping_rules = Column(Text, nullable=True)
    return_policy = Column(Text, nullable=True)

    # Feature toggles
    enabled_tools = Column(JSON, default=lambda: [
        "search_products",
        "get_product",
        "check_inventory",
        "get_product_variants",
        "get_order",
        "create_order",
        "update_order",
        "calculate_shipping",
        "get_shipping_status",
        "capture_lead",
        "create_support_ticket",
        "transfer_to_human"
    ], nullable=False)

    handoff_rules = Column(JSON, default=lambda: {
        "auto_escalate_complaints": True,
        "auto_escalate_refunds": True,
        "low_confidence_threshold": 0.5,
        "transfer_keywords": ["human", "agent", "manager", "support", "talk to person", "manush"]
    }, nullable=False)

    business_hours = Column(JSON, default=lambda: {
        "enabled": False,
        "start_time": "09:00",
        "end_time": "22:00",
        "timezone": "Asia/Dhaka",
        "outside_hours_message": "Our sales team is currently offline, but our AI assistant is here to take your order!"
    }, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
