from langchain_core.messages import HumanMessage, ToolMessage
from backend.src.llm import get_llm
from backend.src.tools.calculator import calculate

def test_tool_calling_cycle():
    """Verify that the LLM invokes the calculator tool and integrates the output."""
    # 1. Initialize LLM and bind the tool
    llm = get_llm(temperature=0.0)
    tools = [calculate]
    llm_with_tools = llm.bind_tools(tools)
    
    # 2. Ask a question requiring exact math
    messages = [
        HumanMessage(content="What is (1250 * 8) + 475? Use the calculate tool.")
    ]
    
    # Step A: LLM decides to call the tool
    ai_response = llm_with_tools.invoke(messages)
    messages.append(ai_response)
    
    print("\n--- Step 1: LLM Tool Call Decision ---")
    print(f"Tool calls requested: {ai_response.tool_calls}")
    assert len(ai_response.tool_calls) > 0, "LLM should have called the calculate tool"
    
    tool_call = ai_response.tool_calls[0]
    assert tool_call["name"] == "calculate"
    
    # Step B: Execute the tool locally in Python
    tool_output = calculate.invoke(tool_call["args"])
    print(f"Tool execution result: {tool_output}")
    
    # Step C: Send the ToolMessage back to the LLM
    tool_message = ToolMessage(
        content=str(tool_output),
        tool_call_id=tool_call["id"]
    )
    messages.append(tool_message)
    
    # Step D: LLM generates the final answer
    final_response = llm_with_tools.invoke(messages)
    safe_content = final_response.content.encode("ascii", "replace").decode("ascii")
    print("\n--- Step 2: Final Answer from LLM ---")
    print(safe_content)
    print("-------------------------------------")
    
    assert "10475" in final_response.content or "10,475" in final_response.content
    print("\nSUCCESS: Full Tool Calling Cycle Verified!")

if __name__ == "__main__":
    test_tool_calling_cycle()
