import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.src.main import app
from backend.src.schemas import PlanOutput, SubTask, EvaluationOutput
from backend.src.graph import build_aura_graph
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

MOCK_PLAN = PlanOutput(
    summary="Comparison between React and Vue",
    subtasks=[
        SubTask(
            id=1,
            title="React Architecture",
            description="Investigate React JSX and component model",
            category="technical",
            priority=1,
            search_query="React component architecture",
            target_aspects=["Virtual DOM", "JSX"]
        ),
        SubTask(
            id=2,
            title="Vue Reactivity",
            description="Investigate Vue reactivity system",
            category="technical",
            priority=2,
            search_query="Vue 3 reactivity proxy",
            target_aspects=["Reactivity", "Composition API"]
        )
    ]
)

MOCK_EVAL_GOOD = EvaluationOutput(
    status="GOOD",
    reason="All architecture dimensions thoroughly evaluated.",
    missing_information=[]
)

MOCK_SEARCH_RESULTS = [
    {
        "title": "React Documentation",
        "url": "https://react.dev",
        "content": "React lets you build user interfaces out of individual pieces called components.",
        "is_fallback": False
    },
    {
        "title": "Vue.js Documentation",
        "url": "https://vuejs.org",
        "content": "Vue is a progressive JavaScript framework built on top of standard HTML, CSS and JavaScript.",
        "is_fallback": False
    }
]


@patch("backend.src.agents.planner.safe_llm_invoke")
@patch("backend.src.agents.researcher.web_search")
@patch("backend.src.agents.researcher.safe_llm_invoke")
@patch("backend.src.agents.analyst.safe_llm_invoke")
@patch("backend.src.agents.evaluator.safe_llm_invoke")
@patch("backend.src.agents.responder.safe_llm_invoke")
def test_full_graph_execution_mocked(
    mock_responder,
    mock_evaluator,
    mock_analyst,
    mock_researcher_llm,
    mock_search,
    mock_planner
):
    """Test full LangGraph traversal with zero external API dependencies."""
    mock_planner.return_value = MOCK_PLAN
    mock_search.invoke.return_value = MOCK_SEARCH_RESULTS
    
    mock_summary_resp = MagicMock()
    mock_summary_resp.content = "Both frameworks provide high performance component systems."
    mock_researcher_llm.return_value = mock_summary_resp
    
    mock_analysis_resp = MagicMock()
    mock_analysis_resp.content = "Executive Summary: React uses JSX while Vue uses template syntax."
    mock_analyst.return_value = mock_analysis_resp
    
    mock_evaluator.return_value = MOCK_EVAL_GOOD
    
    mock_final_resp = MagicMock()
    mock_final_resp.content = "Comprehensive Comparison: React vs Vue."
    mock_responder.return_value = mock_final_resp

    # Execute graph
    graph = build_aura_graph()
    initial_state = {
        "original_query": "Compare React vs Vue for modern web apps",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }

    result = graph.invoke(initial_state)
    assert result["original_query"] == "Compare React vs Vue for modern web apps"
    assert len(result["subtasks"]) == 2
    assert len(result["research_results"]) == 2
    assert "React" in result["analysis"]
    assert result["evaluation"].status == "GOOD"
    assert len(result["final_answer"]) > 10


@patch("backend.src.agents.planner.safe_llm_invoke")
@patch("backend.src.agents.researcher.web_search")
@patch("backend.src.agents.researcher.safe_llm_invoke")
@patch("backend.src.agents.analyst.safe_llm_invoke")
@patch("backend.src.agents.evaluator.safe_llm_invoke")
@patch("backend.src.agents.responder.safe_llm_invoke")
def test_post_research_api_and_db_mocked(
    mock_responder,
    mock_evaluator,
    mock_analyst,
    mock_researcher_llm,
    mock_search,
    mock_planner
):
    """Test POST /api/research endpoint and SQLite database persistence."""
    mock_planner.return_value = MOCK_PLAN
    mock_search.invoke.return_value = MOCK_SEARCH_RESULTS
    
    mock_summary_resp = MagicMock()
    mock_summary_resp.content = "Summary of research findings."
    mock_researcher_llm.return_value = mock_summary_resp
    
    mock_analysis_resp = MagicMock()
    mock_analysis_resp.content = "Comparative analysis of options."
    mock_analyst.return_value = mock_analysis_resp
    
    mock_evaluator.return_value = MOCK_EVAL_GOOD
    
    mock_final_resp = MagicMock()
    mock_final_resp.content = "Final synthesized research report."
    mock_responder.return_value = mock_final_resp

    res = client.post("/api/research", json={"query": "Compare React vs Vue"})
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert data["query"] == "Compare React vs Vue"
    assert len(data["subtasks"]) == 2
    assert len(data["sources"]) == 2

    # Verify SQLite persistence
    db = TestingSessionLocal()
    saved = db.query(ResearchRun).filter(ResearchRun.id == data["id"]).first()
    assert saved is not None
    assert saved.query == "Compare React vs Vue"
    db.close()
