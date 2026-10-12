# AURA Project Task Tracker

## Status Legend
- `[ ]` Not Started
- `[-]` In Progress
- `[x]` Completed

---

## Phase 1 — Foundations
- [x] **Task 1: Project Setup & Environment**
  - **Objective**: Set up Python virtual environment, directory layout, `.gitignore`, and `.env` template.
  - **Concepts**: Virtual environments, dependency management, API key security.
  - **Files**: `.gitignore`, `.env.example`, `requirements.txt`
  - **Status**: `[x] Completed`
  - **Dependencies**: None

- [x] **Task 2: First LLM API Call**
  - **Objective**: Initialize a LangChain chat model wrapper and execute a basic prompt/response.
  - **Concepts**: LLM APIs, System/Human messages, Temperature, Token usage.
  - **Files**: `backend/src/llm.py`, `backend/tests/test_llm.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 1

- [x] **Task 3: Structured LLM Output**
  - **Objective**: Force the LLM to return strictly typed JSON conforming to a Pydantic schema.
  - **Concepts**: Pydantic models, JSON schemas, Instructor / `with_structured_output`, parsing guarantees.
  - **Files**: `backend/src/schemas.py`, `backend/src/structured_llm.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 2

- [x] **Task 4: Tool Calling Fundamentals**
  - **Objective**: Build a custom calculator tool and bind it to the LLM.
  - **Concepts**: Tool definitions, tool schemas (JSON Schema), function calling, tool message handling.
  - **Files**: `backend/src/tools/calculator.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 3

- [x] **Task 5: Web Search Tool Integration**
  - **Objective**: Integrate Tavily search tool to retrieve real-time external web sources.
  - **Concepts**: External search APIs, context retrieval, source attribution/URLs.
  - **Files**: `backend/src/tools/search.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 4

---

## Phase 2 — LangGraph Basics
- [x] **Task 6: LangGraph Fundamentals**
  - **Objective**: Build a minimal single-node and two-node graph using `StateGraph`.
  - **Concepts**: Graph state, Nodes (Python functions modifying state), Edges (flow control), Graph compilation.
  - **Files**: `backend/src/graph_basics.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 5

- [x] **Task 7: Sequential Chain Graph (User → Planner → Response)**
  - **Objective**: Create a 2-step workflow where the Planner creates subtasks and a Responder outputs them.
  - **Concepts**: State propagation, passing complex lists across nodes.
  - **Files**: `backend/src/chains/planner_chain.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 6

- [x] **Task 8: Research Graph (Planner → Research → Response)**
  - **Objective**: Connect the search tool to a research node executing subtasks.
  - **Concepts**: Dynamic tool execution inside graph nodes, aggregating tool outputs into state.
  - **Files**: `backend/src/chains/research_chain.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 7

- [x] **Task 9: Specialized Research Node Delegation**
  - **Objective**: Allow the graph to handle multiple distinct research areas cleanly.
  - **Concepts**: Subtask mapping, parallel or sequential node execution.
  - **Files**: `backend/src/agents/researcher.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 8

---

## Phase 3 — Multi-Agent System & Iterative Routing
- [x] **Task 10: Planner Agent Implementation**
  - **Objective**: Build a robust Planner Agent that converts complex queries into structured subtasks.
  - **Concepts**: Prompt engineering for task decomposition, structured subtask schemas.
  - **Files**: `backend/src/agents/planner.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 9

- [x] **Task 11: Research Agent Implementation**
  - **Objective**: Build the dedicated Research Agent using Tavily search with query reformulation.
  - **Concepts**: Information retrieval, summarization without hallucination, source preservation.
  - **Files**: `backend/src/agents/researcher.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 10

- [x] **Task 12: Analyst Agent Implementation**
  - **Objective**: Synthesize all research findings, compare data, resolve contradictions, structure analysis.
  - **Concepts**: Information synthesis, reasoning over evidence, grounding checks.
  - **Files**: `backend/src/agents/analyst.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 11

- [x] **Task 13: Evaluator Agent Implementation**
  - **Objective**: Critique the analysis against the user query for completeness, accuracy, and source backing.
  - **Concepts**: Self-reflection, automated evaluation, structured critique schemas (`status: GOOD | NEEDS_RESEARCH`).
  - **Files**: `backend/src/agents/evaluator.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 12

- [x] **Task 14: Conditional Routing & Evaluator Loop**
  - **Objective**: Implement LangGraph conditional edges (`add_conditional_edges`) to route back to research on `NEEDS_RESEARCH`.
  - **Concepts**: Conditional edges, cycle execution in graphs, state persistence across iterations.
  - **Files**: `backend/src/graph.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 13

- [x] **Task 15: Loop Safeguards & Retry Limits**
  - **Objective**: Prevent infinite loops by enforcing max iteration limits in state.
  - **Concepts**: Cycle bounds, fallback transitions, system resilience.
  - **Files**: `backend/src/graph.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 14

---

## Phase 4 — Backend API
- [x] **Task 16: FastAPI Application Initialization**
  - **Objective**: Set up FastAPI server with CORS middleware, lifespan events, and health check.
  - **Concepts**: ASGI, CORS, request/response lifecycle, asynchronous endpoints.
  - **Files**: `backend/src/main.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 15

- [x] **Task 17: Research Endpoint (`POST /research`)**
  - **Objective**: Create the core API endpoint that accepts a query, runs the LangGraph workflow, and returns structured results.
  - **Concepts**: Background tasks vs async execution, streaming events vs final payload response.
  - **Files**: `backend/src/api/routes.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 16

- [x] **Task 18: API Integration Testing**
  - **Objective**: Test endpoint inputs, outputs, and validation errors using `httpx` and `pytest`.
  - **Concepts**: API integration testing, mock requests.
  - **Files**: `backend/tests/test_api.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 17

---

## Phase 5 — Frontend Development
- [x] **Task 19: React + Vite Setup with Tailwind CSS**
  - **Objective**: Initialize clean React frontend with Tailwind CSS.
  - **Concepts**: Component hierarchy, state management in React, responsive design.
  - **Files**: `frontend/`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 18

- [x] **Task 20: Research Input Interface**
  - **Objective**: Build modern input box with submission handling, validation, and sample prompt triggers.
  - **Concepts**: Controlled inputs, form handling.
  - **Files**: `frontend/src/components/InputSection.jsx`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 19

- [x] **Task 21: Agent Execution Timeline / Activity Tracker**
  - **Objective**: Visual stepper showing agent states (`Planner` → `Researcher` → `Analyst` → `Evaluator` → `Final`).
  - **Concepts**: Visual progress indicators, dynamic status badges.
  - **Files**: `frontend/src/components/AgentActivity.jsx`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 20

- [x] **Task 22: Final Answer & Synthesis Display**
  - **Objective**: Render formatted markdown of the synthesized answer with sections and key findings.
  - **Concepts**: Markdown rendering in React, copy-to-clipboard, typography.
  - **Files**: `frontend/src/components/ResponseView.jsx`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 21

- [x] **Task 23: Sources & Citations Component**
  - **Objective**: Display interactive source cards with clickable URLs, domains, and snippet previews.
  - **Concepts**: Source linking, card layouts.
  - **Files**: `frontend/src/components/SourceList.jsx`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 22

- [x] **Task 24: End-to-End Frontend-to-Backend Connection**
  - **Objective**: Wire all frontend states to live FastAPI endpoints.
  - **Concepts**: `fetch` / `axios`, loading states, error boundaries, network retries.
  - **Files**: `frontend/src/App.jsx`, `frontend/src/api/client.js`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 23

---

## Phase 6 — Persistence & History
- [x] **Task 25: SQLite Database Setup & Models**
  - **Objective**: Create SQLite schema with SQLAlchemy / SQLModel to store past research runs, queries, answers, and sources.
  - **Concepts**: Relational data modeling, ORM basics, SQLite lightweight persistence.
  - **Files**: `backend/src/db/models.py`, `backend/src/db/session.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 24

- [x] **Task 26: Research History Endpoints & UI Sidebar**
  - **Objective**: Save each research run to SQLite; display past research history list in the frontend sidebar.
  - **Concepts**: CRUD operations, historical state retrieval.
  - **Files**: `backend/src/api/routes.py`, `frontend/src/components/Sidebar.jsx`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 25

---

## Phase 7 — Reliability, Error Handling & Testing
- [x] **Task 27: LLM & Tool Error Handling**
  - **Objective**: Add graceful fallbacks for rate limits, API timeouts, and missing API keys.
  - **Concepts**: Defensive agent programming, exception handling in async nodes.
  - **Files**: `backend/src/utils/error_handlers.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 26

- [x] **Task 28: Search Tool Failover & Input Sanitization**
  - **Objective**: Handle empty search results or Tavily connection drops gracefully.
  - **Concepts**: Query fallback strategies, error state injection.
  - **Files**: `backend/src/tools/search.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 27

- [x] **Task 29: Structured Output Validation Recovery**
  - **Objective**: Catch JSON parsing errors and use self-correction prompting to repair outputs.
  - **Concepts**: Output parser recovery, schema retry patterns.
  - **Files**: `backend/src/utils/parsers.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 28

- [x] **Task 30: End-to-End Backend Unit & Integration Tests**
  - **Objective**: Write comprehensive test suites for tools, agents, graph routing, and API endpoints.
  - **Concepts**: Pytest fixtures, mocking external API calls (LLM & Tavily), graph execution testing.
  - **Files**: `backend/tests/`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 29

---

## Phase 8 — Polish, Documentation & Interview Prep
- [x] **Task 31: System Architecture Diagram & Technical README**
  - **Objective**: Document exact graph flow, state schemas, API specs, and setup instructions.
  - **Concepts**: Technical writing, architecture documentation, Mermaid diagrams.
  - **Files**: `README.md`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 30

- [x] **Task 32: Execution Metrics & Logging**
  - **Objective**: Add structured logging to measure execution time, total LLM calls, tool invocations, and retry count.
  - **Concepts**: Observability, agent telemetry, performance profiling.
  - **Files**: `backend/src/utils/logger.py`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 31

- [x] **Task 33: Sample Benchmark Queries & Final Interview Walkthrough**
  - **Objective**: Run 3 diverse real-world complex queries and review key interview questions and answers.
  - **Concepts**: System evaluation, interview defense preparation.
  - **Files**: `docs/interview_guide.md`
  - **Status**: `[x] Completed`
  - **Dependencies**: Task 32
