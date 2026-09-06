from sqlalchemy import Column, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class PlanTier(str, enum.Enum):
    FREE = "FREE"
    STARTER = "STARTER"
    BUSINESS = "BUSINESS"
    AGENCY = "AGENCY"


class RoleType(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    VIEWER = "VIEWER"


class Organization(BaseModel):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    plan = Column(String(50), default=PlanTier.STARTER.value, nullable=False)
    currency = Column(String(10), default="BDT", nullable=False)  # BDT, USD, etc.
    timezone = Column(String(50), default="Asia/Dhaka", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    logo_url = Column(String(1024), nullable=True)

    # Relationships
    memberships = relationship("Membership", back_populates="organization", cascade="all, delete-orphan")


class Membership(BaseModel):
    __tablename__ = "memberships"

    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), default=RoleType.AGENT.value, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="memberships")
    user = relationship("User", back_populates="memberships")
