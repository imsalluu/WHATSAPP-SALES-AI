from sqlalchemy import Column, String, Float, ForeignKey, JSON, Text, Integer
from sqlalchemy.orm import relationship
import enum
from app.models.base import TenantModel


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, enum.Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    REFUNDED = "REFUNDED"


class PaymentMethod(str, enum.Enum):
    COD = "COD"          # Cash on Delivery
    BKASH = "BKASH"      # bKash / Mobile Wallet
    NAGAD = "NAGAD"
    CARD = "CARD"
    ONLINE = "ONLINE"


class Order(TenantModel):
    __tablename__ = "orders"

    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True, index=True)
    
    order_number = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(50), default=OrderStatus.PENDING.value, nullable=False, index=True)
    
    subtotal = Column(Float, default=0.0, nullable=False)
    shipping_fee = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    
    payment_method = Column(String(50), default=PaymentMethod.COD.value, nullable=False)
    payment_status = Column(String(50), default=PaymentStatus.UNPAID.value, nullable=False)
    
    delivery_name = Column(String(255), nullable=False)
    delivery_phone = Column(String(50), nullable=False)
    delivery_address = Column(String(1024), nullable=False)
    delivery_city = Column(String(100), nullable=True)
    
    tracking_number = Column(String(100), nullable=True)
    courier_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    conversation = relationship("Conversation", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(TenantModel):
    __tablename__ = "order_items"

    order_id = Column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_variant_id = Column(String(36), ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True)
    
    product_name = Column(String(255), nullable=False)
    variant_name = Column(String(255), nullable=True)
    sku = Column(String(100), nullable=True)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product_variant = relationship("ProductVariant")
