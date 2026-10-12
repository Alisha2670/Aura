from backend.src.chains.research_chain import build_research_chain

def test_research_chain_live_execution():
    """Verify that Planner -> Researcher (Tavily) -> Responder executes end-to-end."""
    chain = build_research_chain()
    
    initial_state = {
        "original_query": "What are the key new features of Python 3.13?",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    print("\n--- Running 3-Node Research Chain (Planner -> Researcher -> Responder) ---")
    result = chain.invoke(initial_state)
    
    print("\n--- Subtasks Researched ---")
    for t in result["subtasks"]:
        safe_title = t.title.encode("ascii", "replace").decode("ascii")
        print(f"  [{t.id}] {safe_title}")
        
    print(f"\nTotal Research Results Gathered: {len(result['research_results'])}")
    
    print("\n--- Final Grounded Answer with Citations ---")
    safe_answer = result["final_answer"].encode("ascii", "replace").decode("ascii")
    print(safe_answer)
    print("---------------------------------------------")
    
    assert len(result["research_results"]) >= 2
    assert "Sources & Citations" in result["final_answer"]
    assert len(result["final_answer"]) > 100
    print("\nSUCCESS: 3-Node Live Research Workflow Verified!")

if __name__ == "__main__":
    test_research_chain_live_execution()
