from backend.src.graph import build_aura_graph

def test_full_aura_workflow():
    """Verify that the full multi-agent graph with conditional routing executes end-to-end."""
    graph = build_aura_graph()
    
    initial_state = {
        "original_query": "Compare Bun vs Node.js for backend API throughput and memory usage",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    print("\n--- Running Full AURA Multi-Agent Graph ---")
    final_state = graph.invoke(initial_state)
    
    print(f"\n1. Subtasks Decomposed: {len(final_state['subtasks'])}")
    print(f"2. Research Evidence Collected: {len(final_state['research_results'])}")
    print(f"3. Iteration Loops Run: {final_state['iteration_count']}")
    print(f"4. Evaluator Final Status: {final_state['evaluation'].status}")
    
    safe_reason = final_state['evaluation'].reason.encode('ascii', 'replace').decode('ascii')
    print(f"   Evaluator Reason: {safe_reason[:150]}...")
    
    print("\n--- Final Grounded Response ---")
    safe_answer = final_state["final_answer"].encode("ascii", "replace").decode("ascii")
    print(safe_answer[:500] + "...\n")
    print("-------------------------------")
    
    assert final_state["evaluation"] is not None
    assert len(final_state["research_results"]) >= 2
    assert len(final_state["final_answer"]) > 100
    assert "Sources & Citations" in final_state["final_answer"]
    print("SUCCESS: AURA Conditional Routing & Multi-Agent Loop Verified!")

if __name__ == "__main__":
    test_full_aura_workflow()
