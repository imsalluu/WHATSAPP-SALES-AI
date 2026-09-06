from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class AgentConfigUpdate(BaseModel):
    agent_name: Optional[str] = None
    personality: Optional[str] = None
    tone: Optional[str] = None
    language: Optional[str] = None
    greeting_message: Optional[str] = None
    custom_system_prompt: Optional[str] = None
    sales_instructions: Optional[str] = None
    business_description: Optional[str] = None
    shipping_rules: Optional[str] = None
    return_policy: Optional[str] = None
    enabled_tools: Optional[List[str]] = None
    handoff_rules: Optional[Dict[str, Any]] = None
    business_hours: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class AgentConfigOut(BaseModel):
    id: str
    organization_id: str
    agent_name: str
    personality: str
    tone: str
    language: str
    greeting_message: str
    custom_system_prompt: Optional[str] = None
    sales_instructions: Optional[str] = None
    business_description: Optional[str] = None
    shipping_rules: Optional[str] = None
    return_policy: Optional[str] = None
    enabled_tools: List[str] = []
    handoff_rules: Dict[str, Any] = {}
    business_hours: Dict[str, Any] = {}
    is_active: bool

    class Config:
        from_attributes = True
