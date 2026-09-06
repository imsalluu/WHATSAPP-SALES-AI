import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_sales_simulator_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "salesagent_test@store.com",
                "password": "Password123!",
                "full_name": "Sales Tester",
                "organization_name": "Apex Trendz",
            },
        )
        token = reg_res.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}

        # Seed products
        await client.post("/api/v1/products/seed-samples", headers=auth_headers)

        # 1. User asks for recommendations under 3000 taka
        msg1 = await client.post(
            "/api/v1/conversations/simulator",
            json={
                "phone_number": "+8801999887766",
                "customer_name": "Rahim Ahmed",
                "message": "I need a gift for my wife under 3000 taka",
            },
            headers=auth_headers,
        )
        assert msg1.status_code == 200
        data1 = msg1.json()
        assert data1["status"] == "AI_ACTIVE"
        assert len(data1["tools_executed"]) > 0
        assert "search_products" in [t["tool"] for t in data1["tools_executed"]]

        # 2. User checks size availability
        msg2 = await client.post(
            "/api/v1/conversations/simulator",
            json={
                "phone_number": "+8801999887766",
                "message": "Is the black hoodie available in XL?",
            },
            headers=auth_headers,
        )
        assert msg2.status_code == 200
        data2 = msg2.json()
        assert "check_inventory" in [t["tool"] for t in data2["tools_executed"]]

        # 3. User requests human handoff
        msg3 = await client.post(
            "/api/v1/conversations/simulator",
            json={
                "phone_number": "+8801999887766",
                "message": "I want to talk to a human agent please",
            },
            headers=auth_headers,
        )
        assert msg3.status_code == 200
        data3 = msg3.json()
        assert data3["status"] == "HUMAN_REQUIRED"
