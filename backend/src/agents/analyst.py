from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.state import ResearchState
from backend.src.utils.error_handlers import safe_llm_invoke

ANALYST_SYSTEM_PROMPT = """You are AURA's Senior Research Analyst Agent.
Your job is to synthesize all gathered research evidence into a rigorous, well-structured, comparative analysis.

Rules for your analysis:
1. STRICTLY GROUNDED: Work ONLY with the facts and numbers present in the research evidence. Do NOT invent specs or extrapolate beyond the provided data.
2. SYNTHESIZE & COMPARE: Do not just repeat each subtask. Compare options side-by-side, highlight trade-offs, and explain the practical implications.
3. CONTRADICTION RESOLUTION: If different sources report different figures, explain why (e.g., base vs upgraded model, regional pricing, testing conditions).
4. CLEAR STRUCTURE: Organize your analysis with:
   - Executive Summary
   - Detailed Technical & Value Comparison
   - Key Trade-offs & Practical Recommendations
   - Uncertainties or Information Gaps (if any data was missing from research)
"""

def analyst_node(state: ResearchState) -> dict:
    """
    Analyst Node: Synthesizes all collected research results into a cohesive analytical report.
    """
    query = state["original_query"]
    results = state.get("research_results", [])
    
    # Format all research packages into a structured dossier
    dossier_blocks = []
    for r in results:
        dossier_blocks.append(
            f"=== Subtask {r['task_id']}: {r['task_title']} ({r['category'].upper()}) ===\n"
            f"Findings:\n{r['summary']}\n"
            f"Target Aspects: {r.get('target_aspects', [])}"
        )
        
    dossier_text = "\n\n".join(dossier_blocks)
    
    prompt = f"""Original User Query: {query}

Comprehensive Research Evidence Dossier:
{dossier_text}

Please produce a comprehensive, structured analysis answering the original user query based strictly on the evidence above."""

    llm = get_llm(temperature=0.0)
    messages = [
        SystemMessage(content=ANALYST_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    analysis_response = safe_llm_invoke(llm, messages)
    
    return {
        "analysis": analysis_response.content
    }
