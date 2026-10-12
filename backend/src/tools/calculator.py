import numexpr
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """
    Useful for performing mathematical calculations.
    Accepts mathematical expressions as a string (e.g. '45 * 12 + 100').
    Returns the numeric result.
    """
    try:
        # Evaluate mathematical expressions safely
        result = numexpr.evaluate(expression).item()
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
