from langgraph.graph import StateGraph, START, END
from backend.src.state import ResearchState
from backend.src.schemas import SubTask
from backend.src.agents.planner import planner_node
from backend.src.agents.researcher import researcher_node
from backend.src.agents.analyst import analyst_node
from backend.src.agents.evaluator import evaluator_node
from backend.src.agents.responder import responder_node

# Strict system safeguard: Maximum allowed research loops
MAX_RESEARCH_ITERATIONS = 2

def adaptive_researcher_node(state: ResearchState) -> dict:
    """
    Enhanced Researcher Node:
    - Initial run: Researches Planner's subtasks.
    - Retry loops: Generates dynamic subtasks for missing_information.
    """
    evaluation = state.get("evaluation")
    iteration_count = state.get("iteration_count", 0)
    
    # If looping back because of missing information, create targeted subtasks for the missing items
    if evaluation and evaluation.status == "NEEDS_RESEARCH" and evaluation.missing_information:
        existing_subtasks = state.get("subtasks", [])
        start_id = len(existing_subtasks) + 1
        
        new_subtasks = []
        for i, missing_item in enumerate(evaluation.missing_information[:2]):  # Cap to top 2 missing items
            new_subtasks.append(
                SubTask(
                    id=start_id + i,
                    title=f"Retry: {missing_item[:40]}",
                    description=f"Specifically uncover: {missing_item}",
                    category="general",
                    priority=1,
                    search_query=missing_item[:80]
                )
            )
            
        retry_state = dict(state)
        retry_state["subtasks"] = new_subtasks
        update = researcher_node(retry_state)
        
        combined_results = state.get("research_results", []) + update["research_results"]
        combined_subtasks = existing_subtasks + new_subtasks
        
        return {
            "research_results": combined_results,
            "subtasks": combined_subtasks,
            "iteration_count": iteration_count + 1
        }
    else:
        update = researcher_node(state)
        update["iteration_count"] = iteration_count + 1
        return update

def route_after_evaluation(state: ResearchState) -> str:
    """
    Conditional Routing Function with Strict Loop Safeguard.
    """
    evaluation = state.get("evaluation")
    iteration_count = state.get("iteration_count", 0)
    
    # Condition 1: Research meets high quality standard
    if evaluation and evaluation.status == "GOOD":
        return "responder"
        
    # Condition 2: Max iteration safeguard reached -> prevent infinite loop
    if iteration_count >= MAX_RESEARCH_ITERATIONS:
        return "responder"
        
    # Condition 3: Safe to execute one retry loop
    return "researcher"

def build_aura_graph():
    """
    Assembles and compiles the full AURA Autonomous Multi-Agent Research Graph with safeguards:
    START ──> planner ──> researcher ──> analyst ──> evaluator ──(conditional + bound)──> responder ──> END
                               ▲                             │
                               └──────── NEEDS_RESEARCH ─────┘
    """
    workflow = StateGraph(ResearchState)
    
    # Register Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", adaptive_researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("responder", responder_node)
    
    # Fixed Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "evaluator")
    
    # Conditional Edge with Bound Check
    workflow.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "responder": "responder",
            "researcher": "researcher"
        }
    )
    
    workflow.add_edge("responder", END)
    
    return workflow.compile()
