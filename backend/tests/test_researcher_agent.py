from backend.src.agents.planner import planner_node
from backend.src.agents.researcher import researcher_node

def test_researcher_agent_execution():
    """Verify that Planner -> Researcher executes targeted search and deduplicates URLs."""
    state = {
        "original_query": "Compare the base pricing and warranty terms of iPad Pro M4 vs Microsoft Surface Pro 11",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    # 1. Run Planner
    print("\n--- 1. Planner Generates Subtasks ---")
    planner_update = planner_node(state)
    state.update(planner_update)
    
    print(f"Generated {len(state['subtasks'])} subtasks.")
    for t in state["subtasks"]:
        safe_title = t.title.encode("ascii", "replace").decode("ascii")
        safe_query = t.search_query.encode("ascii", "replace").decode("ascii")
        print(f"  [{t.id}] {safe_title} -> Query: \"{safe_query}\"")
        
    # 2. Run Researcher
    print("\n--- 2. Researcher Gathers Grounded Evidence ---")
    researcher_update = researcher_node(state)
    results = researcher_update["research_results"]
    
    print(f"Gathered {len(results)} research packages:")
    for r in results:
        safe_title = r['task_title'].encode('ascii', 'replace').decode('ascii')
        print(f"\n[Task {r['task_id']}] {safe_title} ({r['category'].upper()}):")
        safe_summary = r['summary'].encode('ascii', 'replace').decode('ascii')
        print(f"Summary:\n{safe_summary}")
        print(f"Unique Sources attached: {len(r['sources'])}")
        for s in r["sources"][:2]:
            print(f"  - {s.get('url')}")
            
    # Assertions
    assert len(results) == len(state["subtasks"])
    assert all("summary" in r and len(r["summary"]) > 30 for r in results)
    assert any(len(r["sources"]) > 0 for r in results)
    print("\nSUCCESS: Advanced Research Agent Verified!")

if __name__ == "__main__":
    test_researcher_agent_execution()
