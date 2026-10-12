from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.state import ResearchState
from backend.src.utils.error_handlers import safe_llm_invoke

RESPONDER_SYSTEM_PROMPT = """You are AURA's Final Synthesis Agent.
Your job is to take the gathered research findings and synthesize a comprehensive, well-structured, factual answer.
Group findings clearly by topic, and provide clear citations and source links."""

def responder_node(state: ResearchState) -> dict:
    """
    Responder Node: Synthesizes gathered research into a polished final response with sources.
    """
    query = state["original_query"]
    research_results = state.get("research_results", [])
    
    # Format research context
    research_context_blocks = []
    all_sources = []
    
    for item in research_results:
        research_context_blocks.append(f"### Subtask: {item['task_title']}\n{item['summary']}")
        for src in item.get("sources", []):
            if src.get("url") and src not in all_sources:
                all_sources.append(src)
                
    research_context = "\n\n".join(research_context_blocks)
    
    prompt = f"""User Question: {query}

Gathered Research Findings:
{research_context}

Please generate a final, polished, and structured response answering the user's question directly based on the research evidence."""

    llm = get_llm(temperature=0.0)
    messages = [
        SystemMessage(content=RESPONDER_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]
    
    response = safe_llm_invoke(llm, messages)
    
    # Append sources section
    sources_section = "\n\n### Sources & Citations:\n" + "\n".join(
        [f"- [{s.get('title', 'Source')}]({s.get('url', '')})" for s in all_sources[:5] if s.get('url')]
    )
    
    final_output = response.content + sources_section
    return {
        "final_answer": final_output
    }
