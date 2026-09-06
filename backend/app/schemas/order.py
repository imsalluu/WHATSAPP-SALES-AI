from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class OrderItemInput(BaseModel):
    product_variant_id: Optional[str] = None
    product_name: str
    variant_name: Optional[str] = None
    sku: Optional[str] = None
    unit_price: float
    quantity: int = 1


class OrderItemOut(BaseModel):
    id: str
    order_id: str
    product_variant_id: Optional[str] = None
    product_name: str
    variant_name: Optional[str] = None
    sku: Optional[str] = None
    unit_price: float
    quantity: int
    total_price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_phone: str
    customer_name: str
    delivery_address: str
    delivery_city: Optional[str] = "Dhaka"
    items: List[OrderItemInput]
    payment_method: str = "COD"
    shipping_fee: float = 60.0
    discount: float = 0.0
    notes: Optional[str] = None
    conversation_id: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
    tracking_number: Optional[str] = None
    courier_name: Optional[str] = None


class OrderOut(BaseModel):
    id: str
    organization_id: str
    customer_id: str
    conversation_id: Optional[str] = None
    order_number: str
    status: str
    subtotal: float
    shipping_fee: float
    discount: float
    total_amount: float
    payment_method: str
    payment_status: str
    delivery_name: str
    delivery_phone: str
    delivery_address: str
    delivery_city: Optional[str] = None
    tracking_number: Optional[str] = None
    courier_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
