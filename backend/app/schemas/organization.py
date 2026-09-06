from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.schemas.auth import UserOut


class OrganizationBase(BaseModel):
    name: str
    currency: str = "BDT"
    timezone: str = "Asia/Dhaka"


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    logo_url: Optional[str] = None


class OrganizationOut(OrganizationBase):
    id: str
    slug: str
    plan: str
    is_active: bool
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class MembershipOut(BaseModel):
    id: str
    role: str
    user: UserOut

    class Config:
        from_attributes = True


class InviteMemberRequest(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "AGENT"
