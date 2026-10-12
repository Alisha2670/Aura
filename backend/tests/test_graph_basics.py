from backend.src.graph_basics import build_basic_graph

def test_basic_graph_execution():
    """Verify end-to-end execution of our first LangGraph workflow."""
    graph = build_basic_graph()
    
    initial_state = {
        "user_query": "Compare React vs Vue for building agent dashboards",
        "plan": None,
        "subtasks": [],
        "final_output": ""
    }
    
    print("\n--- Executing LangGraph Workflow ---")
    final_state = graph.invoke(initial_state)
    
    print("\n--- Final Graph State Result ---")
    safe_output = final_state["final_output"].encode("ascii", "replace").decode("ascii")
    print(safe_output)
    print("---------------------------------")
    
    # Assertions
    assert final_state["plan"] is not None
    assert len(final_state["subtasks"]) >= 2
    assert len(final_state["final_output"]) > 0
    print("\nSUCCESS: LangGraph Basic Graph Verified!")

if __name__ == "__main__":
    test_basic_graph_execution()
