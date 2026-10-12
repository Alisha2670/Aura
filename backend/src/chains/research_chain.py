from langgraph.graph import StateGraph, START, END
from backend.src.state import ResearchState
from backend.src.agents.planner import planner_node
from backend.src.agents.researcher import researcher_node
from backend.src.agents.responder import responder_node

def build_research_chain():
    """
    Assembles the 3-node research workflow:
    START ──> planner ──> researcher ──> responder ──> END
    """
    builder = StateGraph(ResearchState)
    
    # 1. Register Nodes
    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("responder", responder_node)
    
    # 2. Register Edges
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "responder")
    builder.add_edge("responder", END)
    
    # 3. Compile
    return builder.compile()
