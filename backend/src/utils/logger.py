import time
import logging
from typing import Dict, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("AURA_Telemetry")


class TelemetryTracker:
    """Collects and aggregates performance metrics across agent nodes and tools."""
    
    def __init__(self, query: str = ""):
        self.query = query
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.node_durations: Dict[str, float] = {}
        self.llm_calls: int = 0
        self.tool_calls: int = 0
        self.retry_count: int = 0

    def record_node_duration(self, node_name: str, duration: float):
        self.node_durations[node_name] = round(duration, 3)

    def increment_llm_call(self):
        self.llm_calls += 1

    def increment_tool_call(self):
        self.tool_calls += 1

    def increment_retry(self):
        self.retry_count += 1

    def finalize(self) -> Dict[str, Any]:
        self.end_time = time.time()
        total_duration = round(self.end_time - self.start_time, 2)
        
        telemetry = {
            "query": self.query,
            "total_execution_seconds": total_duration,
            "llm_calls_total": self.llm_calls,
            "tool_calls_total": self.tool_calls,
            "retry_count": self.retry_count,
            "node_breakdown": self.node_durations
        }
        
        logger.info(f"[Telemetry Report] Completed in {total_duration}s | LLM calls: {self.llm_calls} | Tool queries: {self.tool_calls}")
        return telemetry


def track_node_execution(node_name: str):
    """Decorator to measure and log execution time of a LangGraph agent node."""
    def decorator(func):
        def wrapper(state, *args, **kwargs):
            start = time.time()
            logger.info(f"[Node Start] Executing '{node_name}'...")
            result = func(state, *args, **kwargs)
            duration = round(time.time() - start, 3)
            logger.info(f"[Node Complete] '{node_name}' finished in {duration}s")
            return result
        return wrapper
    return decorator
