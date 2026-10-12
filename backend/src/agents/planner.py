from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.schemas import PlanOutput
from backend.src.state import ResearchState
from backend.src.utils.error_handlers import safe_llm_invoke

PLANNER_SYSTEM_PROMPT = """You are AURA's expert Strategic Research Planner.
Your mission is to break down complex user questions into 2 to 3 high-impact, actionable research subtasks.

Rules for planning:
1. FOCUS & BREVITY: Create strictly 2 to 3 distinct subtasks covering the most critical dimensions of the query.
2. KEYWORD OPTIMIZATION: For each subtask, generate a concise, keyword-rich 'search_query' designed for web search engines.
3. TARGET ASPECTS: List 2 specific key metrics or comparison points.
4. CATEGORIZATION: Assign the correct category ('technical', 'pricing', 'performance', 'general').
5. PRIORITY: Assign priority 1 for core answers, priority 2 for supporting details.
"""

def planner_node(state: ResearchState) -> dict:
    """
    Planner Node: Analyzes user query and decomposes it into high-precision subtasks.
    """
    query = state["original_query"]
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(PlanOutput)
    
    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=f"Create a focused 2-3 step research plan for this query:\n'{query}'")
    ]
    
    plan: PlanOutput = safe_llm_invoke(structured_llm, messages)
    
    return {
        "plan": plan,
        "subtasks": plan.subtasks
    }
