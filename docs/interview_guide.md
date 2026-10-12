# 🎓 AURA — Senior AI Engineer Technical Interview Guide & Benchmark Dossier

---

## 🔬 Benchmark Case Studies & Evaluation Traces

### Benchmark 1: Architectural Trade-off Analysis
- **User Query**: *"Compare FastAPI vs Go Fiber for high-concurrency microservices."*
- **Planner Decomposition**:
  1. `FastAPI Concurrency Model` (Python asyncio, uvloop, event loop throughput limits, GIL considerations).
  2. `Go Fiber Concurrency Model` (Goroutines, memory footprint per request, fasthttp engine).
  3. `Developer Velocity & Ecosystem` (Pydantic validation, OpenAPI generation vs Go static typing).
- **Researcher Retrieval**: Fetched official benchmarks from TechEmpower, FastAPI docs, and Fiber benchmarks with URL deduplication.
- **Analyst Synthesis**: Compared throughput (req/sec), p99 latency under 10k connections, and code maintainability.
- **Evaluator Outcome**: `GOOD` (Score: 9/10).
- **Iterations Taken**: 1.

---

### Benchmark 2: Market, Model & Pricing Evaluation
- **User Query**: *"Analyze pricing and latency tradeoffs between Claude 3.5 Sonnet and GPT-4o."*
- **Planner Decomposition**:
  1. `Input & Output Token Costs` (Price per million input/output tokens, batch discounts).
  2. `Latency & Throughput Specs` (Time-to-first-token TTFT, tokens per second output).
  3. `Coding & Reasoning Benchmarks` (HumanEval, SWE-bench verified scores).
- **Researcher Retrieval**: Fetched latest Anthropic and OpenAI pricing tables and LMSYS leaderboards.
- **Evaluator Outcome**: `GOOD` (Score: 10/10).
- **Iterations Taken**: 1.

---

### Benchmark 3: Multi-Agent System Strategy
- **User Query**: *"What are the state-of-the-art multi-agent framework patterns in 2025?"*
- **Planner Decomposition**:
  1. `Graph State Machines vs Hierarchical Agents` (LangGraph vs CrewAI vs AutoGen).
  2. `Self-Reflection & Human-in-the-Loop` (Critique-revise cycles, guardrail interrupts).
- **Evaluator Outcome**: `GOOD` (Score: 9/10).
- **Iterations Taken**: 1.

---

## 💼 Senior Agentic AI Engineer Interview Defense Q&A

### Q1: Why did you choose LangGraph over traditional linear chains or basic ReAct loops?
**Answer**: Single-prompt ReAct agents suffer from *context drift*, *compounding hallucinations*, and *unpredictable termination* when tasks require multiple distinct cognitive skills. 

By orchestrating the workflow with **LangGraph**, we enforce clean separation of concerns:
- The **Planner** only decomposes queries into structured subtasks with Pydantic typing.
- The **Researcher** only retrieves grounded facts without answering the top-level query.
- The **Analyst** synthesizes across subtasks without hallucinating external facts.
- The **Evaluator** objectively critiques the output.

This graph-based state machine produces deterministic, repeatable execution paths with explicit cycle limits.

---

### Q2: How did you safeguard the system against runaway loops and token explosions?
**Answer**: In `backend/src/graph.py`, we implement conditional edges with two strict criteria:
1. If the Evaluator returns `GOOD`, route immediately to synthesis.
2. If the Evaluator returns `NEEDS_RESEARCH`, check `iteration_count < MAX_RESEARCH_ITERATIONS (2)`. If the limit is reached, force transition to final synthesis with an explicit uncertainty disclosure note. This guarantees bounded costs and deterministic execution time.

---

### Q3: How do you handle production API rate limits (e.g. Groq 429 TPM limits)?
**Answer**: We built an exponential backoff decorator with randomized jitter in `backend/src/utils/error_handlers.py`. It dynamically intercepts `429` status codes and `APITimeoutError`, computing:
$$\text{delay} = \min(\text{base\_delay} \times 2^{\text{attempt}}, \text{max\_delay}) + \text{jitter}$$
This avoids thundering herd problems and recovers transient network dropouts automatically.

---

### Q4: How is persistence architected between the running state and the database?
**Answer**: During execution, graph state resides in an immutable typed dictionary (`ResearchState`). Upon reaching the terminal node, the complete execution payload (structured plan, grounded sources, evaluation scores, and markdown response) is serialized and persisted to SQLite via SQLAlchemy 2.0. This allows users to review past dossiers in the React frontend without consuming LLM tokens.

---

### Q5: How do you prevent search tool failures from breaking the pipeline?
**Answer**: In `backend/src/tools/search.py`, we built a two-tier defense:
1. **Input Sanitization**: Cleans markdown noise and limits query length to $\le 180$ characters.
2. **Automated Fallback**: If a query returns 0 results, it simplifies the query to its core nouns and retries automatically before returning a structured fallback object.
