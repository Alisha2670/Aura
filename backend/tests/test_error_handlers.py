import pytest
from backend.src.utils.error_handlers import retry_with_exponential_backoff, safe_llm_invoke


def test_retry_on_rate_limit_success():
    call_count = 0

    @retry_with_exponential_backoff(max_retries=3, base_delay=0.01, jitter=False)
    def flaky_llm_call():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("429 Rate limit reached for model tokens per minute")
        return {"result": "success"}

    res = flaky_llm_call()
    assert res == {"result": "success"}
    assert call_count == 3


def test_retry_on_timeout_success():
    call_count = 0

    @retry_with_exponential_backoff(max_retries=3, base_delay=0.01, jitter=False)
    def timeout_call():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise Exception("Connection timeout while contacting server")
        return "connected"

    res = timeout_call()
    assert res == "connected"
    assert call_count == 2


def test_retry_exhaustion_raises():
    call_count = 0

    @retry_with_exponential_backoff(max_retries=2, base_delay=0.01, jitter=False)
    def always_failing_call():
        nonlocal call_count
        call_count += 1
        raise Exception("429 Rate limit exceeded")

    with pytest.raises(Exception) as exc_info:
        always_failing_call()

    assert "429 Rate limit exceeded" in str(exc_info.value)
    assert call_count == 3  # initial attempt + 2 retries


def test_non_retryable_error_fails_immediately():
    call_count = 0

    @retry_with_exponential_backoff(max_retries=3, base_delay=0.01, jitter=False)
    def syntax_error_call():
        nonlocal call_count
        call_count += 1
        raise ValueError("Invalid user input parameter")

    with pytest.raises(ValueError):
        syntax_error_call()

    assert call_count == 1  # No retries on ValueError
