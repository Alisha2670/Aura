from backend.src.agents.planner import planner_node
from backend.src.agents.researcher import researcher_node
from backend.src.agents.analyst import analyst_node

def test_planner_researcher_analyst_pipeline():
    """Verify that Planner -> Researcher -> Analyst executes and generates a structured analysis."""
    state = {
        "original_query": "Compare Docker vs Podman for rootless container deployment in enterprise Linux environments",
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    # 1. Planner
    print("\n--- 1. Planner Decomposes Query ---")
    state.update(planner_node(state))
    print(f"Subtasks planned: {len(state['subtasks'])}")
    for t in state["subtasks"]:
        safe_title = t.title.encode("ascii", "replace").decode("ascii")
        print(f"  [{t.id}] {safe_title}")
    
    # 2. Researcher
    print("\n--- 2. Researcher Gathers Grounded Evidence ---")
    state.update(researcher_node(state))
    print(f"Research packages collected: {len(state['research_results'])}")
    
    # 3. Analyst
    print("\n--- 3. Analyst Synthesizes Evidence ---")
    state.update(analyst_node(state))
    
    print("\n--- Generated Analysis ---")
    safe_analysis = state["analysis"].encode("ascii", "replace").decode("ascii")
    print(safe_analysis[:600] + "...\n")
    print("--------------------------")
    
    # Assertions
    assert len(state["analysis"]) > 200
    assert "Executive Summary" in state["analysis"] or "Comparison" in state["analysis"]
    print("SUCCESS: Analyst Agent Synthesis Pipeline Verified!")

if __name__ == "__main__":
    test_planner_researcher_analyst_pipeline()
