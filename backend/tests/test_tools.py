import pytest
from app.models.organization import Organization
from app.models.product import Product, ProductVariant
from app.tools.sales_tools import SalesTools
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_all_sales_tools():
    async with TestingSessionLocal() as db:
        # Create test organization
        org = Organization(name="Test Org", slug="test-tools-org")
        db.add(org)
        await db.flush()

        tools = SalesTools(db=db, organization_id=org.id)

        # 1. Seed a product
        prod = Product(
            organization_id=org.id,
            name="Black Streetwear Hoodie",
            sku="HD-01",
            category="Clothing",
            price=2200.0,
            discount_price=1800.0,
            description="High quality fleece hoodie.",
            is_available=True,
        )
        db.add(prod)
        await db.flush()

        variant = ProductVariant(
            organization_id=org.id,
            product_id=prod.id,
            sku="HD-01-XL",
            title="Black / XL",
            size="XL",
            color="Black",
            stock_quantity=15,
            is_available=True,
        )
        db.add(variant)
        await db.commit()

        # 2. Test search_products
        s_res = await tools.search_products(query="hoodie", max_price=2000.0)
        assert s_res["status"] == "success"
        assert len(s_res["products"]) >= 1

        # 3. Test check_inventory
        inv_res = await tools.check_inventory(product_id_or_sku="HD-01", size="XL", color="Black")
        assert inv_res["status"] == "success"
        assert inv_res["in_stock"] is True
        assert inv_res["stock_quantity"] == 15

        # 4. Test calculate_shipping
        ship_res = await tools.calculate_shipping(city="Dhaka")
        assert ship_res["shipping_fee"] == 60.0

        # 5. Test create_order
        ord_res = await tools.create_order(
            customer_name="Fahim Khan",
            customer_phone="+8801811223344",
            delivery_address="House 12, Road 4, Dhanmondi, Dhaka",
            delivery_city="Dhaka",
            items=[{"product_name": "Black Streetwear Hoodie", "variant_name": "Black / XL", "quantity": 1, "unit_price": 1800.0}],
            payment_method="COD",
        )
        assert ord_res["status"] == "success"
        assert ord_res["total_amount"] == 1860.0  # 1800 + 60 shipping
        assert "order_number" in ord_res

        # 6. Test get_order
        get_ord_res = await tools.get_order(ord_res["order_number"])
        assert get_ord_res["status"] == "success"
        assert get_ord_res["order"]["total_amount"] == 1860.0

        # 7. Test capture_lead
        lead_res = await tools.capture_lead(
            phone="+8801811223344",
            name="Fahim Khan",
            intent="PURCHASE_CONFIRMED",
            lead_score=95,
        )
        assert lead_res["status"] == "success"
        assert lead_res["lead_score"] == 95

        # 8. Test human handoff
        handoff_res = await tools.transfer_to_human(reason="Customer requested manager")
        assert handoff_res["status"] == "escalated"
