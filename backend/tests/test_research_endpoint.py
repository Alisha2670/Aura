import pytest
import httpx
from backend.src.main import app

@pytest.mark.asyncio
async def test_post_research_endpoint():
    """Verify that POST /api/research executes the full graph and returns structured telemetry."""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", timeout=60.0) as client:
        payload = {
            "query": "Compare Vite vs Webpack for React application build times"
        }
        
        print("\n--- Sending POST /api/research Request ---")
        response = await client.post("/api/research", json=payload)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        
        data = response.json()
        print(f"Query: {data['query']}")
        print(f"Subtasks planned: {len(data['subtasks'])}")
        print(f"Research packages: {len(data['research_results'])}")
        print(f"Evaluator Status: {data['evaluation']['status']}")
        print(f"Execution Time: {data['execution_time_seconds']}s")
        
        safe_answer = data['final_answer'].encode('ascii', 'replace').decode('ascii')
        print(f"\nFinal Answer Preview:\n{safe_answer[:350]}...\n")
        
        assert len(data["subtasks"]) >= 2
        assert len(data["research_results"]) >= 2
        assert len(data["final_answer"]) > 50
        assert data["execution_time_seconds"] > 0
        print("SUCCESS: POST /api/research Endpoint Verified!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_post_research_endpoint())
