from backend.src.agents.evaluator import evaluator_node
from backend.src.schemas import SubTask, EvaluationOutput

def test_evaluator_pass_and_fail_scenarios():
    """Verify that Evaluator approves complete analyses and catches incomplete analyses."""
    
    # Scenario 1: INCOMPLETE ANALYSIS (Missing Pricing)
    print("\n--- 1. Testing INCOMPLETE Analysis (Should return NEEDS_RESEARCH) ---")
    incomplete_state = {
        "original_query": "Compare MacBook Air M3 vs Dell XPS 13 on battery life and exact US starting price",
        "plan": None,
        "subtasks": [
            SubTask(id=1, title="Battery Life", description="Compare battery runtime", search_query="battery runtime"),
            SubTask(id=2, title="Starting Price", description="Find exact US starting price", search_query="starting price")
        ],
        "research_results": [
            {
                "task_id": 1,
                "task_title": "Battery Life",
                "summary": "MacBook Air M3 gets 18h, Dell XPS 13 gets 15h.",
                "sources": [{"url": "https://techreview.com"}]
            }
        ],
        "analysis": "The MacBook Air M3 gets about 18 hours of battery life, while the Dell XPS 13 gets around 15 hours. We could not find any pricing information for either laptop.",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    eval_result_fail = evaluator_node(incomplete_state)
    evaluation_fail: EvaluationOutput = eval_result_fail["evaluation"]
    
    safe_reason_fail = evaluation_fail.reason.encode("ascii", "replace").decode("ascii")
    print(f"Status: {evaluation_fail.status}")
    print(f"Reason: {safe_reason_fail}")
    print(f"Missing Information: {evaluation_fail.missing_information}")
    
    assert evaluation_fail.status == "NEEDS_RESEARCH"
    assert len(evaluation_fail.missing_information) > 0
    print("[PASS] Successfully caught missing information!")
    
    # Scenario 2: COMPLETE ANALYSIS (Fully Answered & Grounded)
    print("\n--- 2. Testing COMPLETE Analysis (Should return GOOD) ---")
    complete_state = {
        "original_query": "What is the official release date and major feature of Python 3.13?",
        "plan": None,
        "subtasks": [
            SubTask(id=1, title="Release Date", description="Find release date", search_query="python 3.13 release date"),
            SubTask(id=2, title="Major Features", description="Find major features", search_query="python 3.13 features")
        ],
        "research_results": [
            {
                "task_id": 1,
                "task_title": "Release Date",
                "summary": "Official Python documentation confirms Python 3.13 was released on October 7, 2024.",
                "sources": [{"title": "Python.org", "url": "https://docs.python.org/3.13/whatsnew/3.13.html"}]
            },
            {
                "task_id": 2,
                "task_title": "Major Features",
                "summary": "Key features confirmed in PEP 703 (Free-threaded CPython without GIL) and PEP 744 (JIT compiler).",
                "sources": [{"title": "PEP 703", "url": "https://peps.python.org/pep-0703/"}]
            }
        ],
        "analysis": "Python 3.13 was officially released on October 7, 2024. Its major headline features include experimental Free-threaded CPython without the GIL (PEP 703) and an experimental JIT compiler (PEP 744).",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    eval_result_pass = evaluator_node(complete_state)
    evaluation_pass: EvaluationOutput = eval_result_pass["evaluation"]
    
    safe_reason_pass = evaluation_pass.reason.encode("ascii", "replace").decode("ascii")
    print(f"Status: {evaluation_pass.status}")
    print(f"Reason: {safe_reason_pass}")
    
    assert evaluation_pass.status == "GOOD"
    assert len(evaluation_pass.missing_information) == 0
    print("[PASS] Successfully approved complete analysis!")
    
    print("\nSUCCESS: Evaluator Agent Self-Reflection Verified!")

if __name__ == "__main__":
    test_evaluator_pass_and_fail_scenarios()
