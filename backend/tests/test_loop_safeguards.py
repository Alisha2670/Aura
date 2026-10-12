from backend.src.graph import build_aura_graph, MAX_RESEARCH_ITERATIONS

def test_loop_safeguards_with_high_ambiguity_query():
    """Verify that the graph strictly obeys MAX_RESEARCH_ITERATIONS and never loops infinitely."""
    graph = build_aura_graph()
    
    # Query with deliberately unreleased/secret targets
    initial_state = {
        "original_query": "What are the unreleased internal hardware specifications of Apple M6 chip?",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    print("\n--- Running Graph on Ambiguous/Unreleased Target ---")
    final_state = graph.invoke(initial_state)
    
    print(f"\nFinal Iteration Count: {final_state['iteration_count']}")
    print(f"Max Allowed Limit: {MAX_RESEARCH_ITERATIONS}")
    print(f"Evaluator Status: {final_state['evaluation'].status}")
    
    print("\n--- Graceful Final Response ---")
    safe_answer = final_state["final_answer"].encode("ascii", "replace").decode("ascii")
    print(safe_answer[:400] + "...\n")
    print("-------------------------------")
    
    # Assertions
    assert final_state["iteration_count"] <= MAX_RESEARCH_ITERATIONS, "Graph exceeded max iteration limit!"
    assert len(final_state["final_answer"]) > 50
    print("SUCCESS: Loop Safeguards & Retry Bounds Verified!")

if __name__ == "__main__":
    test_loop_safeguards_with_high_ambiguity_query()
