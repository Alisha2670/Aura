import pytest
from langchain_core.messages import SystemMessage, HumanMessage
from backend.src.llm import get_llm

def test_llm_connection():
    """Verify that the configured LLM connects and responds correctly."""
    llm = get_llm(temperature=0.0)
    
    messages = [
        SystemMessage(content="You are AURA, an AI research assistant."),
        HumanMessage(content="Explain what an AI agent is in exactly one short sentence.")
    ]
    
    response = llm.invoke(messages)
    
    print("\n--- LLM Response ---")
    print(response.content)
    print("--------------------")
    
    assert response.content is not None
    assert len(response.content.strip()) > 0

if __name__ == "__main__":
    test_llm_connection()
