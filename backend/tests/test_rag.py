import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_rag_knowledge_pipeline():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "rag_tester@store.com",
                "password": "Password123!",
                "full_name": "RAG Tester",
                "organization_name": "Velvet Fashion",
            },
        )
        token = reg_res.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}

        # 1. Upload Knowledge Document
        doc_payload = {
            "title": "Return and Exchange Policy 2026",
            "document_type": "RETURN_REFUND",
            "content": "Customers can exchange unworn products within 7 calendar days with original tags attached. Returns for refunds are processed within 3-5 business days via bKash or original payment method. Delivery charge for replacement is complimentary for defective items.",
        }
        create_res = await client.post("/api/v1/knowledge/documents", json=doc_payload, headers=auth_headers)
        assert create_res.status_code == 200
        doc_data = create_res.json()
        assert doc_data["total_chunks"] >= 1

        # 2. Test Semantic Search
        search_res = await client.post(
            "/api/v1/knowledge/search",
            json={"query": "How many days for return or exchange?", "limit": 2},
            headers=auth_headers,
        )
        assert search_res.status_code == 200
        results = search_res.json()
        assert len(results) >= 1
        assert "7 calendar days" in results[0]["content"]
