from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.schemas import EvaluationOutput
from backend.src.state import ResearchState
from backend.src.utils.error_handlers import safe_llm_invoke

EVALUATOR_SYSTEM_PROMPT = """You are AURA's expert Quality Assurance & Evaluator Agent.
Your job is to objectively critique the drafted research analysis against the original user query and gathered evidence.

Your Evaluation Criteria:
1. COMPLETENESS: Does the analysis answer ALL dimensions of the user's question?
2. GROUNDING & ACCURACY: Are claims supported by factual evidence from the research results?
3. GAPS & UNCERTAINTIES: Are any key comparisons, numbers, or critical subtasks missing or unaddressed?

Decision Rules:
- Return status = "GOOD" if the analysis thoroughly and accurately answers the original question based on the supporting evidence.
- Return status = "NEEDS_RESEARCH" if vital information, prices, specs, or subtasks are missing or left incomplete.
- If status is "NEEDS_RESEARCH", provide a clear list of specific 'missing_information' topics that must be researched.
"""

def evaluator_node(state: ResearchState) -> dict:
    """
    Evaluator Node: Critiques the drafted analysis against query, subtasks, and supporting evidence.
    """
    query = state["original_query"]
    analysis = state.get("analysis", "")
    subtasks = state.get("subtasks", [])
    research_results = state.get("research_results", [])
    
    subtasks_summary = "\n".join([f"- Task {t.id} ({t.title}): {t.description}" for t in subtasks])
    
    # Format evidence summary concisely
    evidence_blocks = []
    for r in research_results:
        summary_snippet = r.get('summary', '')[:300]
        sources_count = len(r.get("sources", []))
        evidence_blocks.append(
            f"Subtask {r.get('task_id', '')} ({r.get('task_title', '')}): {summary_snippet}\n"
            f"Sources: {sources_count} attached"
        )
    evidence_summary = "\n\n".join(evidence_blocks) if evidence_blocks else "No research evidence provided."
    
    prompt = f"""Original User Query:
{query}

Subtasks Expected:
{subtasks_summary}

Supporting Research Evidence Gathered:
{evidence_summary}

Drafted Analysis from Analyst:
{analysis}

Please rigorously evaluate this analysis against the original question, planned subtasks, and supporting evidence."""

    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(EvaluationOutput)
    
    messages = [
        SystemMessage(content=EVALUATOR_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    evaluation: EvaluationOutput = safe_llm_invoke(structured_llm, messages)
    
    return {
        "evaluation": evaluation
    }
