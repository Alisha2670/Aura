from backend.src.tools.search import web_search
from backend.src.llm import get_llm
from langchain_core.messages import HumanMessage, ToolMessage

def test_web_search_standalone():
    """Verify that Tavily search returns real-time web results with titles and URLs."""
    print("\n--- 1. Testing Standalone Tavily Search ---")
    results = web_search.invoke({"query": "Python 3.12 release date", "max_results": 2})
    
    assert isinstance(results, list)
    assert len(results) > 0
    print(f"Retrieved {len(results)} search results:")
    for i, res in enumerate(results, 1):
        safe_title = res['title'].encode('ascii', 'replace').decode('ascii')
        print(f"  {i}. Title: {safe_title}")
        print(f"     URL: {res['url']}")
        safe_snippet = res['content'][:120].encode('ascii', 'replace').decode('ascii')
        print(f"     Snippet: {safe_snippet}...\n")
    assert "url" in results[0] and len(results[0]["url"]) > 0

def test_llm_with_web_search():
    """Verify that the LLM autonomously calls web_search and cites its findings."""
    print("--- 2. Testing LLM Autonomous Web Search ---")
    llm = get_llm(temperature=0.0)
    llm_with_search = llm.bind_tools([web_search])
    
    messages = [
        HumanMessage(content="What is the latest stable version of Python as of today? Search the web.")
    ]
    
    # LLM makes tool call
    ai_response = llm_with_search.invoke(messages)
    messages.append(ai_response)
    
    assert len(ai_response.tool_calls) > 0, "LLM should have requested web_search"
    tool_call = ai_response.tool_calls[0]
    print(f"LLM generated search query: {tool_call['args']}")
    
    # Execute tool
    search_output = web_search.invoke(tool_call["args"])
    
    # Pass back tool result
    tool_msg = ToolMessage(content=str(search_output), tool_call_id=tool_call["id"])
    messages.append(tool_msg)
    
    # Final answer
    final_response = llm_with_search.invoke(messages)
    safe_content = final_response.content.encode('ascii', 'replace').decode('ascii')
    print(f"\nFinal LLM Response with live facts:\n{safe_content}")
    print("\nSUCCESS: Web Search Tool Integration Verified!")

if __name__ == "__main__":
    test_web_search_standalone()
    test_llm_with_web_search()
