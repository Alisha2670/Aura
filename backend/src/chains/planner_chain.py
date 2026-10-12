from langgraph.graph import StateGraph, START, END
from backend.src.state import ResearchState
from backend.src.agents.planner import planner_node
from backend.src.agents.responder import responder_node

def build_planner_chain():
    """
    Assembles the modular sequential workflow:
    START ──> planner ──> responder ──> END
    """
    builder = StateGraph(ResearchState)
    
    # 1. Register Nodes
    builder.add_node("planner", planner_node)
    builder.add_node("responder", responder_node)
    
    # 2. Register Edges
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "responder")
    builder.add_edge("responder", END)
    
    # 3. Compile
    return builder.compile()
