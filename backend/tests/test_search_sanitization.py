import pytest
from backend.src.tools.search import sanitize_search_query, web_search


def test_sanitize_search_query_special_chars():
    dirty_query = '**"FastAPI"** vs `Go Fiber` (2025 performance benchmarks?)'
    cleaned = sanitize_search_query(dirty_query)
    assert "*" not in cleaned
    assert '"' not in cleaned
    assert "`" not in cleaned
    assert "(" not in cleaned
    assert ")" not in cleaned
    assert "FastAPI vs Go Fiber 2025 performance benchmarks?" in cleaned


def test_sanitize_search_query_empty_or_none():
    assert sanitize_search_query("") == "general technology overview"
    assert sanitize_search_query(None) == "general technology overview"
    assert sanitize_search_query("   ") == "general technology overview"


def test_sanitize_search_query_truncation():
    super_long = "word " * 60
    cleaned = sanitize_search_query(super_long)
    assert len(cleaned) <= 180


def test_web_search_returns_list_structure():
    # Test that invoking tool returns a list of dictionaries with expected keys
    results = web_search.invoke({"query": "Python asyncio vs threading", "max_results": 2})
    assert isinstance(results, list)
    assert len(results) >= 1
    assert "title" in results[0]
    assert "url" in results[0]
    assert "content" in results[0]
    assert "is_fallback" in results[0]
