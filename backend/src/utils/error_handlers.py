import time
import random
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AURA_Resilience")


def retry_with_exponential_backoff(
    max_retries: int = 4,
    base_delay: float = 2.0,
    max_delay: float = 30.0,
    jitter: bool = True,
):
    """
    Decorator for robustly executing LLM & Tool calls with exponential backoff on rate limits/timeouts.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    err_str = str(e).lower()
                    is_rate_limit = "429" in err_str or "rate limit" in err_str or "tpm" in err_str or "tokens per minute" in err_str
                    is_timeout = "timeout" in err_str or "connection" in err_str

                    if (is_rate_limit or is_timeout) and retries < max_retries:
                        retries += 1
                        delay = min(base_delay * (2 ** (retries - 1)), max_delay)
                        if jitter:
                            delay += random.uniform(0.5, 1.5)

                        logger.warning(
                            f"[Resilience] Encountered {e.__class__.__name__} ({str(e)[:100]}...). "
                            f"Retrying attempt {retries}/{max_retries} in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"[Resilience] Fatal or exhausted retries for {func.__name__}: {str(e)}")
                        raise e
        return wrapper
    return decorator


@retry_with_exponential_backoff(max_retries=4, base_delay=3.0)
def safe_llm_invoke(chain_or_model, input_payload):
    """Safely invokes an LLM or LangChain runnable with built-in retry resilience."""
    return chain_or_model.invoke(input_payload)
