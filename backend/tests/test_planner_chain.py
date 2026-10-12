from backend.src.chains.planner_chain import build_planner_chain

def test_modular_planner_chain():
    """Verify that the modular planner chain executes and updates the state correctly."""
    chain = build_planner_chain()
    
    initial_state = {
        "original_query": "Compare AWS Lambda vs Google Cloud Functions for low-latency microservices",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    print("\n--- Running Modular Planner Chain ---")
    result = chain.invoke(initial_state)
    
    print("\n--- Plan Summary ---")
    safe_summary = result['plan'].summary.encode('ascii', 'replace').decode('ascii')
    print(f"Summary: {safe_summary}")
    print(f"Subtasks count: {len(result['subtasks'])}")
    for t in result["subtasks"]:
        safe_title = t.title.encode('ascii', 'replace').decode('ascii')
        print(f"  [{t.id}] {safe_title}")
        
    print("\n--- Final Answer from Responder ---")
    safe_answer = result["final_answer"].encode("ascii", "replace").decode("ascii")
    print(safe_answer[:300] + "...\n")
    print("-----------------------------------")
    
    assert result["plan"] is not None
    assert len(result["subtasks"]) >= 2
    assert len(result["final_answer"]) > 50
    print("SUCCESS: Modular Sequential Planner Chain Verified!")

if __name__ == "__main__":
    test_modular_planner_chain()
