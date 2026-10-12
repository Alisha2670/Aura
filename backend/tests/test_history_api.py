import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.src.main import app
from backend.src.db.models import Base, ResearchRun
from backend.src.db.session import get_db

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_history_endpoints():
    db = TestingSessionLocal()
    
    # Pre-seed a research run
    run = ResearchRun(
        query="Compare Redis and Memcached",
        response="Redis supports complex data structures while Memcached is simple key-value.",
        iteration_count=1
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    run_id = run.id
    db.close()

    # 1. Test GET /api/history
    res = client.get("/api/history")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1
    assert any(item["id"] == run_id for item in items)

    # 2. Test GET /api/history/{id}
    res_item = client.get(f"/api/history/{run_id}")
    assert res_item.status_code == 200
    data = res_item.json()
    assert data["id"] == run_id
    assert data["query"] == "Compare Redis and Memcached"

    # 3. Test DELETE /api/history/{id}
    del_res = client.delete(f"/api/history/{run_id}")
    assert del_res.status_code == 200
    assert del_res.json()["deleted"] is True

    # 4. Confirm 404 after deletion
    get_after = client.get(f"/api/history/{run_id}")
    assert get_after.status_code == 404
