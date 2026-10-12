import pytest
import httpx
from backend.src.main import app

@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Verify that the FastAPI /api/health endpoint returns status 200 and 'online'."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")
        
        print("\n--- Health Check API Response ---")
        print(f"Status Code: {response.status_code}")
        print(f"Payload: {response.json()}")
        print("---------------------------------")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "AURA" in data["service"]
        print("SUCCESS: FastAPI Server & Health Probe Verified!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_health_check_endpoint())
