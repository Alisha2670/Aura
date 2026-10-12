from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm
from backend.src.tools.search import web_search
from backend.src.state import ResearchState
from backend.src.utils.error_handlers import safe_llm_invoke

CATEGORY_SYSTEM_PROMPTS = {
    "technical": """You are AURA's Technical Research Specialist.
Extract exact hardware/software specifications, architecture details, and compatibility.
Keep bullet points concise and factual.""",

    "pricing": """You are AURA's Pricing & Market Analyst.
Extract current base prices, tier costs, and currency figures.
Always include exact amounts concisely.""",

    "performance": """You are AURA's Benchmark & Performance Specialist.
Extract concrete benchmark figures, runtimes, and latency numbers with clear units.""",

    "general": """You are AURA's General Research Specialist.
Provide an objective, structured summary of key facts and core differences."""
}

def researcher_node(state: ResearchState) -> dict:
    """
    Research Node: Executes targeted searches for each subtask, verifies target aspects,
    deduplicates sources, and records structured evidence.
    """
    subtasks = state.get("subtasks", [])
    collected_results: List[Dict[str, Any]] = []
    seen_urls = set()
    
    llm = get_llm(temperature=0.0)
    
    for task in subtasks:
        category = getattr(task, "category", "general")
        system_prompt = CATEGORY_SYSTEM_PROMPTS.get(category, CATEGORY_SYSTEM_PROMPTS["general"])
        
        # Step A: Use optimized search query with max_results=2 for token efficiency
        query = getattr(task, "search_query", f"{task.title} {task.description}")
        raw_sources = web_search.invoke({"query": query, "max_results": 2})
        
        # Step B: Deduplicate sources by URL
        unique_sources = []
        for src in raw_sources:
            url = src.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append(src)
            elif not url:
                unique_sources.append(src)
                
        # Step C: Prepare compact snippets (max 350 chars per snippet)
        snippets_text = "\n\n".join(
            [f"Source [{s.get('title', 'N/A')}]:\nSnippet: {s.get('content', '')[:350]}" 
             for s in (unique_sources if unique_sources else raw_sources)]
        )
        
        target_aspects_list = getattr(task, "target_aspects", [])
        aspects_str = "\n".join([f"- {a}" for a in target_aspects_list]) if target_aspects_list else "Key factual details"
        
        user_prompt = f"""Subtask: {task.title}
Target Aspects:
{aspects_str}

Search Evidence:
{snippets_text}

Provide 2 concise factual bullet points summarizing the findings."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        summary_response = safe_llm_invoke(llm, messages)
        
        collected_results.append({
            "task_id": task.id,
            "task_title": task.title,
            "category": category,
            "priority": getattr(task, "priority", 1),
            "summary": summary_response.content,
            "sources": unique_sources if unique_sources else raw_sources,
            "target_aspects": target_aspects_list
        })
        
    return {
        "research_results": collected_results
    }
