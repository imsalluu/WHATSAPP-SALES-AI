from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from app.models.base import TenantModel


class Customer(TenantModel):
    __tablename__ = "customers"

    phone_number = Column(String(50), index=True, nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(1024), nullable=True)
    city = Column(String(100), nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    customer_metadata = Column(JSON, default=dict, nullable=False)

    # Relationships
    conversations = relationship("Conversation", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="customer", cascade="all, delete-orphan")
