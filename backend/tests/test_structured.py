import sys
from backend.src.llm import get_llm
from backend.src.schemas import PlanOutput
from langchain_core.messages import SystemMessage, HumanMessage

def test_structured_plan_generation():
    """Verify that the LLM generates a strictly validated PlanOutput object."""
    # 1. Initialize base LLM
    llm = get_llm(temperature=0.0)
    
    # 2. Bind the Pydantic schema using with_structured_output
    structured_llm = llm.with_structured_output(PlanOutput)
    
    # 3. Invoke with a sample user query
    messages = [
        SystemMessage(content="You are AURA's Planner. Break down the user's query into 2 to 3 logical research subtasks."),
        HumanMessage(content="Compare the battery life and price of MacBook Air M3 vs Dell XPS 13.")
    ]
    
    result: PlanOutput = structured_llm.invoke(messages)
    
    # 4. Verify and print results
    print("\n--- Structured Plan Output ---")
    print(f"Plan Summary: {result.summary}")
    print(f"Total Subtasks: {len(result.subtasks)}")
    for task in result.subtasks:
        safe_title = task.title.encode("ascii", "replace").decode("ascii")
        safe_desc = task.description.encode("ascii", "replace").decode("ascii")
        print(f"  [{task.id}] {safe_title}: {safe_desc}")
    print("------------------------------")
    
    # Assertions
    assert isinstance(result, PlanOutput)
    assert len(result.subtasks) >= 2
    assert all(isinstance(t.id, int) for t in result.subtasks)
    print("\nSUCCESS: All Pydantic assertions passed!")

if __name__ == "__main__":
    test_structured_plan_generation()
