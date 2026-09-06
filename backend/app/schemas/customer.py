from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class CustomerBase(BaseModel):
    phone_number: str
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    tags: List[str] = []
    customer_metadata: Dict[str, Any] = {}


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    tags: Optional[List[str]] = None
    customer_metadata: Optional[Dict[str, Any]] = None


class CustomerOut(CustomerBase):
    id: str
    organization_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
