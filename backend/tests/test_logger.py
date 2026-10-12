import time
import pytest
from backend.src.utils.logger import TelemetryTracker, track_node_execution


def test_telemetry_tracker_metrics():
    tracker = TelemetryTracker(query="What is the speed of light?")
    
    tracker.increment_llm_call()
    tracker.increment_llm_call()
    tracker.increment_tool_call()
    tracker.increment_retry()
    tracker.record_node_duration("planner", 0.45)
    tracker.record_node_duration("researcher", 1.25)
    
    metrics = tracker.finalize()
    
    assert metrics["query"] == "What is the speed of light?"
    assert metrics["llm_calls_total"] == 2
    assert metrics["tool_calls_total"] == 1
    assert metrics["retry_count"] == 1
    assert metrics["node_breakdown"]["planner"] == 0.45
    assert metrics["node_breakdown"]["researcher"] == 1.25
    assert metrics["total_execution_seconds"] >= 0


def test_track_node_execution_decorator():
    @track_node_execution("dummy_node")
    def sample_node(state):
        return {"processed": True, **state}

    result = sample_node({"original_query": "hello"})
    assert result["processed"] is True
    assert result["original_query"] == "hello"
