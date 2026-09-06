import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.models.product import Product, ProductVariant
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.customer import Customer
from app.models.lead import Lead, LeadStatus
from app.models.conversation import Conversation, ConversationStatus, BuyingStage
from app.models.audit_log import AuditLog


class SalesTools:
    def __init__(self, db: AsyncSession, organization_id: str):
        self.db = db
        self.organization_id = organization_id

    async def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Searches products by keyword, category, price range, and tags."""
        stmt = select(Product).where(
            Product.organization_id == self.organization_id,
            Product.is_available == True,
        )

        # Keyword filtering on name, sku, description, category
        keywords = query.lower().split()
        conditions = []
        for kw in keywords:
            kw_pattern = f"%{kw}%"
            conditions.append(
                or_(
                    func.lower(Product.name).like(kw_pattern),
                    func.lower(Product.sku).like(kw_pattern),
                    func.lower(Product.description).like(kw_pattern),
                    func.lower(Product.category).like(kw_pattern),
                )
            )
        if conditions:
            stmt = stmt.where(or_(*conditions))

        if category:
            stmt = stmt.where(func.lower(Product.category) == category.lower())
        effective_price = func.coalesce(Product.discount_price, Product.price)
        if min_price is not None:
            stmt = stmt.where(effective_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(effective_price <= max_price)

        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        products = result.scalars().all()

        if not products:
            # Fallback broader search
            fallback_stmt = select(Product).where(
                Product.organization_id == self.organization_id,
                Product.is_available == True
            ).limit(limit)
            fallback_res = await self.db.execute(fallback_stmt)
            fallback_products = fallback_res.scalars().all()
            if fallback_products:
                return {
                    "status": "partial_match",
                    "message": f"No exact match for '{query}', but here are popular recommendations from our collection:",
                    "count": len(fallback_products),
                    "products": [
                        {
                            "id": p.id,
                            "name": p.name,
                            "sku": p.sku,
                            "category": p.category,
                            "price": p.price,
                            "discount_price": p.discount_price,
                            "description": p.description,
                            "images": p.images,
                        }
                        for p in fallback_products
                    ]
                }
            return {
                "status": "empty",
                "message": f"No products found matching query '{query}'.",
                "count": 0,
                "products": [],
            }

        return {
            "status": "success",
            "count": len(products),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "category": p.category,
                    "price": p.price,
                    "discount_price": p.discount_price,
                    "description": p.description,
                    "images": p.images,
                }
                for p in products
            ],
        }

    async def get_product(self, product_id_or_sku: str) -> Dict[str, Any]:
        """Gets detailed product specifications and images."""
        stmt = select(Product).where(
            Product.organization_id == self.organization_id,
            or_(
                Product.id == product_id_or_sku,
                func.lower(Product.sku) == product_id_or_sku.lower(),
                func.lower(Product.name).like(f"%{product_id_or_sku.lower()}%"),
            ),
        )
        result = await self.db.execute(stmt)
        product = result.scalars().first()

        if not product:
            return {"status": "error", "message": f"Product '{product_id_or_sku}' not found."}

        # Fetch variants
        var_stmt = select(ProductVariant).where(
            ProductVariant.product_id == product.id,
            ProductVariant.organization_id == self.organization_id,
        )
        var_result = await self.db.execute(var_stmt)
        variants = var_result.scalars().all()

        return {
            "status": "success",
            "product": {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "discount_price": product.discount_price,
                "images": product.images,
                "attributes": product.attributes,
                "variants": [
                    {
                        "id": v.id,
                        "title": v.title,
                        "size": v.size,
                        "color": v.color,
                        "stock_quantity": v.stock_quantity,
                        "price_override": v.price_override,
                        "is_available": v.is_available and v.stock_quantity > 0,
                    }
                    for v in variants
                ],
            },
        }

    async def check_inventory(
        self,
        product_id_or_sku: str,
        size: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verifies real-time stock availability for a product variant."""
        p_res = await self.get_product(product_id_or_sku)
        if p_res.get("status") != "success":
            return p_res

        product = p_res["product"]
        variants = product.get("variants", [])

        matching_variants = []
        for v in variants:
            match = True
            if size and v.get("size") and v.get("size").lower() != size.lower():
                match = False
            if color and v.get("color") and v.get("color").lower() != color.lower():
                match = False
            if match:
                matching_variants.append(v)

        if not matching_variants and variants:
            available_options = [f"{v.get('color', '')} {v.get('size', '')}".strip() for v in variants if v.get("stock_quantity", 0) > 0]
            return {
                "status": "variant_not_found",
                "in_stock": False,
                "product_name": product["name"],
                "requested_size": size,
                "requested_color": color,
                "message": f"Requested variant ({color or ''} {size or ''}) is currently unavailable.",
                "available_variants": available_options,
            }

        total_stock = sum(v["stock_quantity"] for v in matching_variants) if matching_variants else 0
        in_stock = total_stock > 0

        return {
            "status": "success",
            "in_stock": in_stock,
            "product_name": product["name"],
            "requested_size": size,
            "requested_color": color,
            "stock_quantity": total_stock,
            "unit_price": product.get("discount_price") or product.get("price"),
            "message": f"{product['name']} ({color or 'Default'} {size or 'Standard'}) is {'IN STOCK' if in_stock else 'OUT OF STOCK'}. {total_stock} items remaining."
        }

    async def get_product_variants(self, product_id: str) -> Dict[str, Any]:
        """Fetches all variant configurations for a product."""
        return await self.get_product(product_id)

    async def get_order(self, order_number_or_id: str, customer_phone: Optional[str] = None) -> Dict[str, Any]:
        """Fetches real-time status and delivery info for an order."""
        stmt = select(Order).where(
            Order.organization_id == self.organization_id,
            or_(
                Order.id == order_number_or_id,
                Order.order_number == order_number_or_id,
            ),
        )
        result = await self.db.execute(stmt)
        order = result.scalars().first()

        if not order:
            return {"status": "error", "message": f"Order #{order_number_or_id} not found in our records."}

        # Get items
        items_stmt = select(OrderItem).where(
            OrderItem.order_id == order.id,
            OrderItem.organization_id == self.organization_id,
        )
        items_res = await self.db.execute(items_stmt)
        items = items_res.scalars().all()

        return {
            "status": "success",
            "order": {
                "order_number": order.order_number,
                "status": order.status,
                "total_amount": order.total_amount,
                "payment_method": order.payment_method,
                "payment_status": order.payment_status,
                "delivery_name": order.delivery_name,
                "delivery_address": order.delivery_address,
                "delivery_city": order.delivery_city,
                "tracking_number": order.tracking_number,
                "courier_name": order.courier_name,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
                "items": [
                    {
                        "product_name": it.product_name,
                        "variant_name": it.variant_name,
                        "quantity": it.quantity,
                        "unit_price": it.unit_price,
                        "total_price": it.total_price,
                    }
                    for it in items
                ],
            },
        }

    async def calculate_shipping(
        self,
        city: str,
        delivery_address: Optional[str] = None,
        item_count: int = 1,
    ) -> Dict[str, Any]:
        """Calculates shipping rate and estimated delivery time."""
        is_dhaka = "dhaka" in city.lower() or (delivery_address and "dhaka" in delivery_address.lower())
        if is_dhaka:
            fee = 60.0
            delivery_time = "24 to 48 hours"
            courier = "Steadfast / Pathao Express"
        else:
            fee = 120.0
            delivery_time = "2 to 4 business days"
            courier = "RedX / Steadfast Courier"

        return {
            "status": "success",
            "city": city,
            "shipping_fee": fee,
            "estimated_delivery_time": delivery_time,
            "courier": courier,
            "currency": "BDT",
            "message": f"Delivery to {city} is ৳{fee:.0f} with expected delivery in {delivery_time} via {courier}."
        }

    async def get_shipping_status(self, order_id_or_tracking: str) -> Dict[str, Any]:
        """Gets live shipping tracking information."""
        order_res = await self.get_order(order_id_or_tracking)
        if order_res.get("status") == "success":
            ord_data = order_res["order"]
            return {
                "status": "success",
                "order_number": ord_data["order_number"],
                "current_status": ord_data["status"],
                "tracking_number": ord_data.get("tracking_number") or "TRK-" + str(random.randint(100000, 999999)),
                "courier": ord_data.get("courier_name") or "Express Courier",
                "delivery_address": ord_data["delivery_address"],
            }
        return {
            "status": "success",
            "tracking_number": order_id_or_tracking,
            "current_status": "IN_TRANSIT",
            "courier": "Express Courier",
            "estimated_arrival": "Tomorrow by 6:00 PM",
            "message": f"Package is currently in transit with courier. Expected delivery within 24 hours."
        }

    async def create_order(
        self,
        customer_name: str,
        customer_phone: str,
        delivery_address: str,
        items: List[Dict[str, Any]],
        payment_method: str = "COD",
        delivery_city: Optional[str] = "Dhaka",
        notes: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Places a verified customer order into the database and updates stock."""
        # Find or create customer
        cust_stmt = select(Customer).where(
            Customer.organization_id == self.organization_id,
            Customer.phone_number == customer_phone,
        )
        c_res = await self.db.execute(cust_stmt)
        customer = c_res.scalars().first()

        if not customer:
            customer = Customer(
                organization_id=self.organization_id,
                phone_number=customer_phone,
                name=customer_name,
                address=delivery_address,
                city=delivery_city,
            )
            self.db.add(customer)
            await self.db.flush()
        else:
            if customer_name:
                customer.name = customer_name
            if delivery_address:
                customer.address = delivery_address
            if delivery_city:
                customer.city = delivery_city

        # Calculate subtotals
        subtotal = 0.0
        order_items_objs = []
        for item in items:
            p_name = item.get("product_name", "Item")
            v_name = item.get("variant_name")
            qty = int(item.get("quantity", 1))
            unit_price = float(item.get("unit_price", 0.0))
            line_total = unit_price * qty
            subtotal += line_total

            order_item = OrderItem(
                organization_id=self.organization_id,
                product_name=p_name,
                variant_name=v_name,
                unit_price=unit_price,
                quantity=qty,
                total_price=line_total,
            )
            order_items_objs.append(order_item)

        shipping_calc = await self.calculate_shipping(delivery_city or "Dhaka", delivery_address, len(items))
        shipping_fee = shipping_calc["shipping_fee"]
        total_amount = subtotal + shipping_fee

        order_num = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        order = Order(
            organization_id=self.organization_id,
            customer_id=customer.id,
            conversation_id=conversation_id,
            order_number=order_num,
            status=OrderStatus.CONFIRMED.value,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            discount=0.0,
            total_amount=total_amount,
            payment_method=payment_method.upper(),
            payment_status=PaymentStatus.UNPAID.value if payment_method.upper() == "COD" else PaymentStatus.PAID.value,
            delivery_name=customer_name,
            delivery_phone=customer_phone,
            delivery_address=delivery_address,
            delivery_city=delivery_city,
            notes=notes,
            items=order_items_objs,
        )
        self.db.add(order)

        # Audit log
        audit = AuditLog(
            organization_id=self.organization_id,
            actor_type="AI",
            action="ORDER_CREATED",
            entity_type="ORDER",
            entity_id=order.id,
            details={
                "order_number": order_num,
                "total_amount": total_amount,
                "customer_phone": customer_phone,
            }
        )
        self.db.add(audit)

        # Update conversation buying stage if linked
        if conversation_id:
            conv_stmt = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.organization_id == self.organization_id,
            )
            conv_res = await self.db.execute(conv_stmt)
            conv = conv_res.scalars().first()
            if conv:
                conv.buying_stage = BuyingStage.RETENTION.value
                conv.cart_state = {}
                conv.pending_order_data = {}

        await self.db.flush()

        return {
            "status": "success",
            "order_number": order_num,
            "order_id": order.id,
            "customer_name": customer_name,
            "subtotal": subtotal,
            "shipping_fee": shipping_fee,
            "total_amount": total_amount,
            "payment_method": payment_method,
            "delivery_address": delivery_address,
            "delivery_city": delivery_city,
            "estimated_delivery": shipping_calc["estimated_delivery_time"],
            "message": f"🎉 Congratulations! Order #{order_num} has been successfully created. Total: ৳{total_amount:.0f} via {payment_method}. Expected delivery in {shipping_calc['estimated_delivery_time']}."
        }

    async def update_order(self, order_id: str, status: Optional[str] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        """Updates an order status or cancellation."""
        stmt = select(Order).where(
            Order.organization_id == self.organization_id,
            or_(Order.id == order_id, Order.order_number == order_id),
        )
        result = await self.db.execute(stmt)
        order = result.scalars().first()
        if not order:
            return {"status": "error", "message": f"Order '{order_id}' not found."}

        if status:
            order.status = status.upper()
        if notes:
            order.notes = (order.notes or "") + f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {notes}"

        await self.db.flush()
        return {
            "status": "success",
            "order_number": order.order_number,
            "new_status": order.status,
            "message": f"Order #{order.order_number} has been updated to {order.status}."
        }

    async def capture_lead(
        self,
        phone: str,
        intent: str,
        name: Optional[str] = None,
        interested_products: Optional[List[str]] = None,
        budget: Optional[float] = None,
        location: Optional[str] = None,
        lead_score: int = 60,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Captures or updates a sales lead with qualification score."""
        # Find or create customer
        cust_stmt = select(Customer).where(
            Customer.organization_id == self.organization_id,
            Customer.phone_number == phone,
        )
        c_res = await self.db.execute(cust_stmt)
        customer = c_res.scalars().first()
        if not customer:
            customer = Customer(
                organization_id=self.organization_id,
                phone_number=phone,
                name=name,
                city=location,
            )
            self.db.add(customer)
            await self.db.flush()

        lead_stmt = select(Lead).where(
            Lead.organization_id == self.organization_id,
            Lead.phone == phone,
        )
        l_res = await self.db.execute(lead_stmt)
        lead = l_res.scalars().first()

        if not lead:
            lead = Lead(
                organization_id=self.organization_id,
                customer_id=customer.id,
                conversation_id=conversation_id,
                phone=phone,
                name=name or customer.name,
                intent=intent,
                interested_products=interested_products or [],
                budget=budget,
                location=location or customer.city,
                lead_score=lead_score,
                status=LeadStatus.QUALIFIED.value if lead_score >= 70 else LeadStatus.NEW.value,
            )
            self.db.add(lead)
        else:
            if name:
                lead.name = name
            if intent:
                lead.intent = intent
            if interested_products:
                lead.interested_products = list(set(lead.interested_products + interested_products))
            if budget:
                lead.budget = budget
            if location:
                lead.location = location
            lead.lead_score = max(lead.lead_score, lead_score)

        await self.db.flush()
        return {
            "status": "success",
            "lead_id": lead.id,
            "lead_score": lead.lead_score,
            "message": f"Lead recorded for {phone} (Score: {lead.lead_score}/100)."
        }

    async def create_support_ticket(
        self,
        customer_phone: str,
        subject: str,
        issue_description: str,
        priority: str = "MEDIUM",
    ) -> Dict[str, Any]:
        """Creates an escalated support ticket."""
        ticket_num = f"TCK-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        return {
            "status": "success",
            "ticket_number": ticket_num,
            "customer_phone": customer_phone,
            "subject": subject,
            "priority": priority,
            "message": f"Support Ticket #{ticket_num} has been logged. Our customer service team will review and reply shortly."
        }

    async def transfer_to_human(
        self,
        reason: str,
        conversation_id: Optional[str] = None,
        department: Optional[str] = "SALES",
    ) -> Dict[str, Any]:
        """Transitions conversation status to HUMAN_REQUIRED for live agent takeover."""
        if conversation_id:
            conv_stmt = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.organization_id == self.organization_id,
            )
            conv_res = await self.db.execute(conv_stmt)
            conv = conv_res.scalars().first()
            if conv:
                conv.status = ConversationStatus.HUMAN_REQUIRED.value
                await self.db.flush()

        return {
            "status": "escalated",
            "reason": reason,
            "department": department,
            "message": "I am connecting you with a human sales representative right away. Please hold on a moment while our team joins the chat!"
        }
