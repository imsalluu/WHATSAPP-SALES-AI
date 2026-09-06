import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Register new user & organization
        reg_payload = {
            "email": "owner@brandstore.com",
            "password": "SecurePassword123!",
            "full_name": "Tariq Ahmed",
            "organization_name": "Aura Lifestyle",
            "phone_number": "+8801711223344",
        }
        res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res.status_code == 200, res.text
        data = res.json()
        assert "access_token" in data
        assert data["email"] == "owner@brandstore.com"
        assert data["organization_name"] == "Aura Lifestyle"
        assert data["role"] == "OWNER"

        token = data["access_token"]

        # 2. Get /me
        me_res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        me_data = me_res.json()
        assert me_data["email"] == "owner@brandstore.com"

        # 3. Login
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "owner@brandstore.com", "password": "SecurePassword123!"},
        )
        assert login_res.status_code == 200
        assert "access_token" in login_res.json()
