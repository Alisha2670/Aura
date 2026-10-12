import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.db.models import Base, ResearchRun


@pytest.fixture
def test_db():
    test_db_url = "sqlite:///:memory:"
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        test_engine.dispose()


def test_research_run_crud(test_db):
    sample_run = ResearchRun(
        query="Test query Postgres vs MySQL",
        response="PostgreSQL is better suited for complex queries.",
        plan_json=json.dumps({"subtasks": [{"title": "Compare SQL DBs"}]}),
        sources_json=json.dumps([{"url": "https://example.com", "snippet": "Postgres is great"}]),
        evaluation_json=json.dumps({"verdict": "GOOD", "score": 9}),
        iteration_count=1,
    )

    test_db.add(sample_run)
    test_db.commit()
    test_db.refresh(sample_run)

    assert sample_run.id is not None
    assert len(sample_run.id) == 36  # UUID length
    assert sample_run.query == "Test query Postgres vs MySQL"
    assert sample_run.iteration_count == 1

    # Query back
    fetched = test_db.query(ResearchRun).filter(ResearchRun.id == sample_run.id).first()
    assert fetched is not None
    assert fetched.query == sample_run.query

    data = fetched.to_dict()
    assert data["id"] == sample_run.id
    assert "created_at" in data
    assert json.loads(data["sources_json"])[0]["url"] == "https://example.com"
