import json
import re
import logging
from typing import Type, TypeVar, Any, Optional, Callable
from pydantic import BaseModel

logger = logging.getLogger("AURA_Parsers")
T = TypeVar("T", bound=BaseModel)


def extract_json_from_text(text: str) -> Optional[dict]:
    """
    Extracts JSON dictionary from raw LLM strings, including markdown blocks and conversational wrappers.
    """
    if not text or not isinstance(text, str):
        return None
    
    # 1. Match ```json ... ``` blocks
    json_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if json_block_match:
        candidate = json_block_match.group(1).strip()
        try:
            return json.loads(candidate)
        except Exception:
            pass

    # 2. Match outermost curly braces { ... }
    brace_match = re.search(r"\{[\s\S]*\}", text)
    if brace_match:
        candidate = brace_match.group(0).strip()
        try:
            return json.loads(candidate)
        except Exception:
            # Clean trailing commas before close braces
            cleaned = re.sub(r",\s*([\}\]])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except Exception:
                pass

    return None


def safe_parse_model(raw_output: Any, model_class: Type[T], fallback_factory: Optional[Callable[[], T]] = None) -> T:
    """
    Safely coerces raw LLM output into a validated Pydantic model instance.
    """
    # Case 1: Already an instance
    if isinstance(raw_output, model_class):
        return raw_output

    # Case 2: Dict object
    if isinstance(raw_output, dict):
        try:
            return model_class.model_validate(raw_output)
        except Exception as e:
            logger.warning(f"[Parser] Dict validation failed for {model_class.__name__}: {e}")

    # Case 3: Raw string
    if isinstance(raw_output, str):
        try:
            parsed_dict = json.loads(raw_output)
            return model_class.model_validate(parsed_dict)
        except Exception:
            extracted = extract_json_from_text(raw_output)
            if extracted:
                try:
                    return model_class.model_validate(extracted)
                except Exception as e:
                    logger.warning(f"[Parser] Extracted JSON validation failed: {e}")

    # Case 4: Fallback
    if fallback_factory:
        logger.warning(f"[Parser] Using fallback factory for {model_class.__name__}")
        return fallback_factory()

    raise ValueError(f"Could not safely parse output into {model_class.__name__}: {str(raw_output)[:150]}")
