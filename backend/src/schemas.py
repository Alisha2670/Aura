from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

class SubTask(BaseModel):
    """Represents a single granular research task decomposed by the Planner."""
    id: int = Field(description="Sequential identifier (e.g. 1, 2, 3)")
    title: str = Field(description="Concise action title of the subtask")
    description: str = Field(description="Detailed instructions of what to uncover")
    category: Literal["technical", "pricing", "performance", "general"] = Field(
        default="general",
        description="Domain category for specialized extraction prompts"
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=3,
        description="Priority level: 1 = Critical/Highest, 2 = Important, 3 = Supplementary"
    )
    search_query: str = Field(
        description="Optimized keyword-based search query formatted specifically for search engines"
    )
    target_aspects: List[str] = Field(
        default_factory=list,
        description="List of specific metrics, specs, or questions this subtask must answer"
    )

class PlanOutput(BaseModel):
    """Structured plan returned by the Planner Agent."""
    summary: str = Field(description="High-level understanding of the user request")
    subtasks: List[SubTask] = Field(description="List of subtasks needed to completely answer the query")

class EvaluationOutput(BaseModel):
    """Structured critique returned by the Evaluator Agent."""
    status: Literal["GOOD", "NEEDS_RESEARCH"] = Field(
        description="GOOD if the findings completely answer the question, or NEEDS_RESEARCH if critical info is missing"
    )
    reason: str = Field(description="Justification for the evaluation decision")
    missing_information: List[str] = Field(
        default_factory=list,
        description="Specific topics or facts that must be researched further if status is NEEDS_RESEARCH"
    )

# --- API Request & Response Schemas ---

class ResearchRequest(BaseModel):
    """Incoming request payload from the frontend."""
    query: str = Field(
        min_length=3,
        max_length=1000,
        description="The research question to decompose and investigate",
        examples=["Compare FastAPI vs Go Fiber for high-concurrency microservices"]
    )

class ResearchResponse(BaseModel):
    """Structured response payload returned to the frontend."""
    query: str
    plan: Optional[PlanOutput]
    subtasks: List[SubTask]
    research_results: List[Dict[str, Any]]
    analysis: str
    evaluation: Optional[EvaluationOutput]
    final_answer: str
    iteration_count: int
    execution_time_seconds: float
