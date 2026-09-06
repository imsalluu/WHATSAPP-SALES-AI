from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class LeadBase(BaseModel):
    phone: str
    name: Optional[str] = None
    intent: Optional[str] = None
    interested_products: List[str] = []
    budget: Optional[float] = None
    location: Optional[str] = None
    lead_score: int = 50
    status: str = "NEW"
    objections: List[str] = []
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    intent: Optional[str] = None
    interested_products: Optional[List[str]] = None
    budget: Optional[float] = None
    location: Optional[str] = None
    lead_score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class LeadOut(LeadBase):
    id: str
    organization_id: str
    customer_id: str
    conversation_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
