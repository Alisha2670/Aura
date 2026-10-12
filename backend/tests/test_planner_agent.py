from backend.src.agents.planner import planner_node

def test_planner_agent_decomposition():
    """Verify that the Planner produces optimized keywords, priorities, and target aspects."""
    state = {
        "original_query": "Compare the performance, RAM limits, and starting prices of MacBook Pro M3 Max vs Lenovo ThinkPad P1 Gen 7 for machine learning workloads.",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    print("\n--- Running Planner Agent Isolated Unit Test ---")
    update = planner_node(state)
    plan = update["plan"]
    subtasks = update["subtasks"]
    
    print(f"\nPlan Summary: {plan.summary}")
    print(f"Total Subtasks: {len(subtasks)}\n")
    
    for t in subtasks:
        safe_title = t.title.encode("ascii", "replace").decode("ascii")
        safe_query = t.search_query.encode("ascii", "replace").decode("ascii")
        print(f"Task {t.id} [Priority {t.priority} | {t.category.upper()}]: {safe_title}")
        print(f"  Search Query: \"{safe_query}\"")
        safe_aspects = [a.encode("ascii", "replace").decode("ascii") for a in t.target_aspects]
        print(f"  Target Aspects: {safe_aspects}\n")
        
    # Assertions
    assert len(subtasks) >= 2
    assert all(hasattr(t, "search_query") and len(t.search_query) > 0 for t in subtasks)
    assert all(hasattr(t, "priority") and 1 <= t.priority <= 3 for t in subtasks)
    assert any(len(t.target_aspects) > 0 for t in subtasks)
    print("SUCCESS: Planner Agent Decomposition Verified!")

if __name__ == "__main__":
    test_planner_agent_decomposition()
