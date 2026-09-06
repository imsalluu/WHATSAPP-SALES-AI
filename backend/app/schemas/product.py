from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class VariantBase(BaseModel):
    sku: str
    title: str
    size: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None
    price_override: Optional[float] = None
    stock_quantity: int = 0
    is_available: bool = True


class VariantCreate(VariantBase):
    pass


class VariantUpdate(BaseModel):
    title: Optional[str] = None
    sku: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None
    price_override: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None


class VariantOut(VariantBase):
    id: str
    product_id: str

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    is_available: bool = True
    tags: List[str] = []
    images: List[str] = []
    attributes: Dict[str, Any] = {}


class ProductCreate(ProductBase):
    variants: List[VariantCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    is_available: Optional[bool] = None
    tags: Optional[List[str]] = None
    images: Optional[List[str]] = None
    attributes: Optional[Dict[str, Any]] = None


class ProductOut(ProductBase):
    id: str
    organization_id: str
    variants: List[VariantOut] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
