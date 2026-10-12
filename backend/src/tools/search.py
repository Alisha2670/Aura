import os
import re
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
from backend.src.utils.error_handlers import retry_with_exponential_backoff

load_dotenv()
logger = logging.getLogger("AURA_Search")


def sanitize_search_query(query: str) -> str:
    """Sanitize and normalize query string for optimal web search engine matching."""
    if not query or not isinstance(query, str):
        return "general technology overview"
    
    # Strip markdown symbols, quotes, and excessive special characters
    cleaned = re.sub(r'[*_`"\'\(\)\[\]\{\}<>]', ' ', query)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Truncate overly verbose queries
    if len(cleaned) > 180:
        cleaned = cleaned[:180].rsplit(' ', 1)[0]
        
    return cleaned if len(cleaned) >= 3 else "general technology overview"


def get_tavily_client() -> TavilyClient:
    """Initialize TavilyClient using TAVILY_API_KEY from environment."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or not api_key.strip() or api_key == "your_tavily_api_key_here":
        raise ValueError("TAVILY_API_KEY not found or empty in .env file.")
    return TavilyClient(api_key=api_key.strip())


@tool
def web_search(query: str, max_results: int = 2) -> List[Dict[str, Any]]:
    """
    Search the web for up-to-date information, specs, and benchmarks.
    Includes automated query sanitization and fallback retry logic.
    """
    sanitized = sanitize_search_query(query)
    
    @retry_with_exponential_backoff(max_retries=3, base_delay=1.5)
    def _execute_search(q: str):
        client = get_tavily_client()
        return client.search(query=q, max_results=max_results, search_depth="basic")

    try:
        response = _execute_search(sanitized)
        results = response.get("results", [])

        # Fallback: If 0 results, retry with simplified core query
        if not results and len(sanitized.split()) > 4:
            simplified_query = " ".join(sanitized.split()[:4])
            logger.info(f"[Search Tool] 0 results for '{sanitized}', falling back to '{simplified_query}'")
            response = _execute_search(simplified_query)
            results = response.get("results", [])

        if not results:
            return [{
                "title": f"No direct matches for {sanitized}",
                "url": "https://duckduckgo.com/?q=" + sanitized.replace(" ", "+"),
                "content": f"No specific web articles found for query '{sanitized}'.",
                "is_fallback": True
            }]

        formatted_sources = []
        for item in results:
            formatted_sources.append({
                "title": item.get("title", "Web Source"),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:400],
                "is_fallback": False
            })
        return formatted_sources

    except Exception as e:
        logger.error(f"[Search Tool] Web search failed: {str(e)}")
        return [{
            "title": "Search Unavailable",
            "url": "",
            "content": f"Live web search temporarily unavailable: {str(e)}",
            "is_fallback": True
        }]
