from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.deps import get_current_organization, require_roles
from app.models.organization import Organization, RoleType
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderOut, OrderCreate, OrderStatusUpdate
from app.tools.sales_tools import SalesTools

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderOut])
async def list_orders(
    status_filter: Optional[str] = None,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Order).where(Order.organization_id == current_org.id)
    if status_filter:
        stmt = stmt.where(Order.status == status_filter.upper())
    stmt = stmt.order_by(Order.created_at.desc())

    result = await db.execute(stmt)
    orders = result.scalars().all()

    orders_out = []
    for ord_obj in orders:
        items_stmt = select(OrderItem).where(OrderItem.order_id == ord_obj.id)
        items_res = await db.execute(items_stmt)
        ord_obj.items = items_res.scalars().all()
        orders_out.append(ord_obj)

    return orders_out


@router.post("/", response_model=OrderOut)
async def create_order(
    data: OrderCreate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    tools = SalesTools(db=db, organization_id=current_org.id)
    items_dicts = [item.model_dump() for item in data.items]
    res = await tools.create_order(
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        delivery_address=data.delivery_address,
        delivery_city=data.delivery_city,
        items=items_dicts,
        payment_method=data.payment_method,
        notes=data.notes,
        conversation_id=data.conversation_id,
    )
    if res.get("status") != "success":
        raise HTTPException(status_code=400, detail=res.get("message"))

    await db.commit()
    # Fetch newly created order
    new_ord_res = await db.execute(select(Order).where(Order.id == res["order_id"]))
    order = new_ord_res.scalars().first()
    items_stmt = select(OrderItem).where(OrderItem.order_id == order.id)
    items_res = await db.execute(items_stmt)
    order.items = items_res.scalars().all()
    return order


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_detail(
    order_id: str,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Order).where(
        Order.organization_id == current_org.id,
        (Order.id == order_id) | (Order.order_number == order_id),
    )
    res = await db.execute(stmt)
    order = res.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items_stmt = select(OrderItem).where(OrderItem.order_id == order.id)
    items_res = await db.execute(items_stmt)
    order.items = items_res.scalars().all()
    return order


@router.patch("/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    current_org: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db),
    _role=Depends(require_roles([RoleType.OWNER.value, RoleType.ADMIN.value, RoleType.AGENT.value])),
):
    stmt = select(Order).where(
        Order.organization_id == current_org.id,
        (Order.id == order_id) | (Order.order_number == order_id),
    )
    res = await db.execute(stmt)
    order = res.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = data.status.upper()
    if data.notes:
        order.notes = (order.notes or "") + f"\n{data.notes}"
    if data.tracking_number:
        order.tracking_number = data.tracking_number
    if data.courier_name:
        order.courier_name = data.courier_name

    await db.commit()
    await db.refresh(order)

    items_stmt = select(OrderItem).where(OrderItem.order_id == order.id)
    items_res = await db.execute(items_stmt)
    order.items = items_res.scalars().all()
    return order
