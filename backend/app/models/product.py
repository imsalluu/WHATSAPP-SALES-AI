from sqlalchemy import Column, String, Float, Boolean, ForeignKey, JSON, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import TenantModel


class Product(TenantModel):
    __tablename__ = "products"

    name = Column(String(255), index=True, nullable=False)
    sku = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), index=True, nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    
    is_available = Column(Boolean, default=True, nullable=False)
    tags = Column(JSON, default=list, nullable=False)
    images = Column(JSON, default=list, nullable=False)  # URLs
    attributes = Column(JSON, default=dict, nullable=False)  # Custom attributes like brand, warranty

    # Relationships
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(TenantModel):
    __tablename__ = "product_variants"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    sku = Column(String(100), index=True, nullable=False)
    title = Column(String(255), nullable=False)  # e.g., "Black / XL"
    size = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    material = Column(String(100), nullable=True)
    price_override = Column(Float, nullable=True)
    stock_quantity = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="variants")
