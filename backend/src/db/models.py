import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ResearchRun(Base):
    """Database model for persisting multi-agent research runs."""
    __tablename__ = "research_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(String(500), nullable=False, index=True)
    response = Column(Text, nullable=False)
    plan_json = Column(Text, nullable=True)
    sources_json = Column(Text, nullable=True)
    evaluation_json = Column(Text, nullable=True)
    iteration_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "response": self.response,
            "plan_json": self.plan_json,
            "sources_json": self.sources_json,
            "evaluation_json": self.evaluation_json,
            "iteration_count": self.iteration_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
