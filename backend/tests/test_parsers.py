import pytest
from backend.src.schemas import EvaluationOutput, PlanOutput, SubTask
from backend.src.utils.parsers import extract_json_from_text, safe_parse_model


def test_extract_json_from_markdown():
    text_with_markdown = """Here is the evaluation:
```json
{
    "status": "GOOD",
    "reason": "The analysis thoroughly covers all query aspects.",
    "missing_information": []
}
```
Hope this helps!"""
    parsed = extract_json_from_text(text_with_markdown)
    assert parsed is not None
    assert parsed["status"] == "GOOD"
    assert "thoroughly" in parsed["reason"]


def test_extract_json_with_trailing_comma():
    dirty_json = """{
        "status": "NEEDS_RESEARCH",
        "reason": "Missing pricing data",
        "missing_information": ["exact pricing tier",],
    }"""
    parsed = extract_json_from_text(dirty_json)
    assert parsed is not None
    assert parsed["status"] == "NEEDS_RESEARCH"


def test_safe_parse_model_from_string():
    raw_str = """```json
    {
        "status": "GOOD",
        "reason": "Complete coverage",
        "missing_information": []
    }
    ```"""
    model = safe_parse_model(raw_str, EvaluationOutput)
    assert isinstance(model, EvaluationOutput)
    assert model.status == "GOOD"


def test_safe_parse_model_fallback():
    garbage = "I am an AI and I cannot generate JSON for this request."
    
    def default_eval():
        return EvaluationOutput(
            status="GOOD",
            reason="Fallback evaluation generated due to parser error",
            missing_information=[]
        )

    recovered = safe_parse_model(garbage, EvaluationOutput, fallback_factory=default_eval)
    assert isinstance(recovered, EvaluationOutput)
    assert recovered.status == "GOOD"
    assert "Fallback" in recovered.reason
