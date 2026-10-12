import pytest
import httpx
from backend.src.main import app

@pytest.mark.asyncio
async def test_api_full_suite():
    """Comprehensive test suite for the FastAPI backend."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", timeout=60.0) as client:
        
        # 1. Test Root Route
        print("\n--- 1. Testing GET / ---")
        root_res = await client.get("/")
        assert root_res.status_code == 200
        assert "AURA API" in root_res.json()["message"]
        print("[PASS] Root endpoint passed (200 OK)")

        # 2. Test Health Check Route
        print("\n--- 2. Testing GET /api/health ---")
        health_res = await client.get("/api/health")
        assert health_res.status_code == 200
        assert health_res.json()["status"] == "online"
        print("[PASS] Health check passed (200 OK)")

        # 3. Test Invalid Request (Query Too Short -> Expected HTTP 422)
        print("\n--- 3. Testing POST /api/research with Invalid Input (Too Short) ---")
        bad_res = await client.post("/api/research", json={"query": "a"})
        print(f"Status: {bad_res.status_code}")
        assert bad_res.status_code == 422, "FastAPI should reject query shorter than 3 characters"
        print("[PASS] Validation error correctly caught with HTTP 422 Unprocessable Entity")

        # 4. Test Missing Query Key (Expected HTTP 422)
        print("\n--- 4. Testing POST /api/research with Missing Body ---")
        missing_res = await client.post("/api/research", json={})
        assert missing_res.status_code == 422
        print("[PASS] Missing field correctly caught with HTTP 422")

        # 5. Test Valid Research Request
        print("\n--- 5. Testing Valid POST /api/research Execution ---")
        valid_payload = {"query": "Compare PyTorch vs JAX for deep learning research"}
        valid_res = await client.post("/api/research", json=valid_payload)
        
        assert valid_res.status_code == 200
        data = valid_res.json()
        
        print(f"Status Code: {valid_res.status_code}")
        print(f"Subtasks returned: {len(data['subtasks'])}")
        print(f"Execution Time: {data['execution_time_seconds']}s")
        assert len(data["subtasks"]) >= 2
        assert len(data["final_answer"]) > 50
        print("[PASS] Valid research pipeline passed (200 OK)")

    print("\n=======================================================")
    print("ALL FASTAPI INTEGRATION TESTS PASSED SUCCESSFULLY! ")
    print("=======================================================")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api_full_suite())
