from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.schemas import PlanOutput, SubTask

# 1. Define the Graph State Schema
class BasicResearchState(TypedDict):
    """The shared blackboard for our graph."""
    user_query: str
    plan: PlanOutput | None
    subtasks: List[SubTask]
    final_output: str

# 2. Node 1: Planner Node
def planner_node(state: BasicResearchState) -> dict:
    """Invokes LLM with structured PlanOutput and updates state."""
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(PlanOutput)
    
    messages = [
        SystemMessage(content="You are AURA's Planner. Decompose the query into 2-3 actionable subtasks."),
        HumanMessage(content=state["user_query"])
    ]
    
    plan: PlanOutput = structured_llm.invoke(messages)
    return {
        "plan": plan,
        "subtasks": plan.subtasks
    }

# 3. Node 2: Formatter Node
def formatter_node(state: BasicResearchState) -> dict:
    """Takes subtasks from state and creates a formatted summary."""
    plan = state["plan"]
    subtasks = state["subtasks"]
    
    lines = [f"Plan Summary: {plan.summary}", "Subtasks generated:"]
    for task in subtasks:
        lines.append(f"  - [{task.id}] {task.title}: {task.description}")
        
    formatted_text = "\n".join(lines)
    return {"final_output": formatted_text}

# 4. Build and Compile the Graph
def build_basic_graph():
    """Assembles and compiles the LangGraph state machine."""
    workflow = StateGraph(BasicResearchState)
    
    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("formatter", formatter_node)
    
    # Add Edges (START -> planner -> formatter -> END)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "formatter")
    workflow.add_edge("formatter", END)
    
    # Compile
    return workflow.compile()
