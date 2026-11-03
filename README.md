# Empório da Música - AI Agent & Evaluation Harness

Technical implementation for the AI Engineer Full Stack technical challenge at Artefact.

This repository provides an enterprise customer service conversational agent for *Empório da Música*, a musical instrument retailer based in Campo Grande, MS, Brazil. The system combines a LangChain ReAct agent orchestrator implemented via LangGraph, Retrieval-Augmented Generation (RAG) over internal store policies, an automated ETL pipeline transforming relational operational records into SQLite, deterministic pre-LLM scope guardrails, multi-turn conversation persistence, a modern dark-mode React/TypeScript frontend with Artefact visual identity, and an automated evaluation harness with benchmark scoring over ground-truth test cases.

---

<img width="1920" height="1080" alt="Empório da Música Chat Interface" src="https://github.com/user-attachments/assets/207afb92-ce5a-4682-8852-755aa828418a" />

<img width="1920" height="1080" alt="Empório da Música Product Recommendations and Financing" src="https://github.com/user-attachments/assets/8fb68b38-0728-4a11-a44e-0a72e9c36b90" />

---

## 1. Architecture and Technical Decisions

The system architecture is structured across six core software and AI engineering pillars:

### 1.1. Agent Orchestration: LangChain ReAct Pattern (LangGraph)
* **Implementation**: Built using `langgraph.prebuilt.create_react_agent`, aligning with current production standards within the LangChain ecosystem.
* **Architectural Rationale**: The ReAct (Reasoning + Acting) architecture creates a closed execution loop of thought, action, and observation. By binding functions decorated with Pydantic type validation (`@tool`), the agent executes multi-step composite workflows deterministically (for example, querying payment policies and stock levels in a single turn) while preserving visibility into intermediate reasoning steps and tool arguments.

### 1.2. LLM Provider Strategy and Resilience
* **Primary Model**: Google Gemini (`gemini-3.5-flash-lite`), integrated through `langchain-google-genai`.
* **Fallback Provider**: OpenAI (`gpt-4o-mini`), configurable via standard environment variables.
* **Deterministic Offline Engine**: A zero-cost mock provider utilized for unit testing and CI/CD pipelines without incurring token costs or rate limits.
* **Architectural Rationale**: `gemini-3.5-flash-lite` delivers sub-second response latencies, robust native Portuguese function calling, and high cost-efficiency for transactional messaging. The provider layer adheres to dependency inversion: switching models or providers is managed entirely through `.env` configurations without modifying application code.

### 1.3. Data Engineering (ETL) and Relational Persistence Layer
* **Data Processing Pipeline (`app/db/etl.py`)**:
  * **Text Sanitization and Normalization**: Unicode NFKC standardization, whitespace stripping, and casing alignment across all operational tables.
  * **Monetary Precision**: Strict conversion and rounding of monetary amounts and discount percentages into two-decimal fixed floating-point numbers.
  * **Inventory Invariants**: Enforcement of non-negative stock constraints (`stock_quantity >= 0`).
  * **Specification Extraction**: Parsing and validation of JSON attribute strings into structured technical specification dictionaries (woods, scale length, pickup configurations, electronic controls).
  * **Campaign Integrity**: Binary segmentation between active campaigns (`is_active = 1`) and expired promotions (`is_active = 0`), enforcing the store rule prohibiting the application of expired discounts.
* **Relational Database Design**:
  * Persistent SQLite backend (`data/emporio.db`) with explicit foreign key enforcement (`PRAGMA foreign_keys = ON;`) and composite query indexing (`idx_products_name`, `idx_products_category`, `idx_products_price`, `idx_orders_customer`, `idx_orders_tracking`).
  * **Session Persistence**: Relational `conversation_history` table indexed by `session_id`, ensuring full message recovery across application restarts and browser reloads.
  * **Roadmap to Dockerized PostgreSQL**: The persistence layer uses decoupled query interfaces. Migrating from local SQLite to containerized PostgreSQL (`docker-compose.yml`) requires modifying only the database connection factory without touching service routes.

### 1.4. Policy Retrieval Architecture (RAG)
* **Knowledge Domain**: Customer Service Policy and Procedure Manual (`data/políticas_da_loja.pdf`, Version 2.1).
* **Retrieval Strategy**: Semantic domain structuring covering operational hours, physical address, Consumer Defense Code (CDC Article 49) 7-day right of withdrawal, 90-day warranty procedures, shipping thresholds, and cash (PIX) discount non-cumulativity over active promotional campaigns.
* **Architectural Rationale**: Prevents hallucination regarding legal deadlines, warranty clauses, and payment policies by injecting verbatim excerpts directly into the agent reasoning context.

### 1.5. Deterministic Scope Guardrails
* **Scope Specification**: As defined in the store operational guidelines, Empório da Música **exclusively sells complete musical instruments** and **does not stock standalone accessories or amplification** (e.g., loose strings, string sets, picks, cables, effect pedals, guitar amplifiers, or standalone cases).
* **Implementation (`app/agent/guardrails.py`)**: A deterministic pre-LLM filter intercepts accessory inquiries and out-of-scope topics (e.g., software programming, recipes, general politics) prior to model invocation, issuing a polite refusal and directing the customer to regional partner shops.
* **Production Impact**: Zero token expenditure and zero model latency on out-of-scope traffic, with 100% deterministic policy adherence.

### 1.6. Frontend Architecture and Technology Stack
The web interface was engineered to provide a responsive, dark-mode Single Page Application (SPA) with persistent session history:
* **React 18**: Core component framework using functional hooks (`useState`, `useEffect`, `useRef`, `useMemo`) for reactive message feed rendering, active session state synchronization, and optimistic UI updates.
* **TypeScript**: Strict static typing across domain models and API contracts (`Message`, `ChatSession`, `ChatResponse`, `HealthResponse`), ensuring end-to-end type safety across client and server boundaries.
* **Tailwind CSS**: Utility-first styling framework implementing a mobile-first responsive grid, custom Artefact corporate magenta accents (`#E60067`), fluid sidebar animations (`w-72` / `w-0` with `overflow-hidden`), and dark theme typography.
* **Marked.js**: Client-side Markdown parser and compiler that dynamically formats catalog listings, pricing matrices, installment schedules, and bulleted specifications with structured alignment and clean typography.
* **HTML5 LocalStorage API**: Browser-level state persistence preserving active session identifiers and chat history lists across browser refreshes (F5), reconciled with the backend SQLite database.
* **Vite & Tooling**: Configured build pipeline in `frontend/` supporting hot module replacement (HMR) during development and production asset bundling.
* **Visual Identity & Vector Graphics**: Vector reproduction of the Artefact brand typography (`tracking-[0.06em]`), geometric chevron glyphs (`/\`), and dedicated avatars for the customer and AI assistant.

---

## 2. Setup and Execution Instructions

### 2.1. Prerequisites
* Python 3.11 or higher (developed and verified on Python 3.12).
* Package manager: `uv` (recommended) or `pip`.

### 2.2. Environment Installation

```bash
# 1. Clone repository
git clone https://github.com/augdev1/artefact_ai_fullstack.git
cd artefact_ai_fullstack

# 2. Setup virtual environment using uv (recommended)
uv venv .venv
uv pip install -e ".[dev]"

# Alternative using standard pip
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2.3. Environment Configuration

Copy the sample environment file:
```bash
cp .env.example .env
```

Configure credentials in `.env`:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

# Optional Fallback Configuration
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini
DATABASE_PATH=data/emporio.db
HOST=0.0.0.0
PORT=8000
```

### 2.4. Running the Full-Stack Application

The FastAPI backend natively serves the React SPA at root:

```bash
python -m app.main
```

Available service endpoints:
* **Conversational Web Application**: http://localhost:8000
* **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
* **API Health Check**: http://localhost:8000/api/health

---

## 3. Evaluation Harness and Testing Suite

The codebase includes an automated test suite comprising 39 tests executed via `pytest`, complemented by a standalone benchmark evaluation runner against a ground-truth dataset (*Golden Dataset*).

### 3.1. Full Test Suite Execution (`pytest`)

```bash
pytest -v
```

Test coverage breakdown:
* `tests/test_database.py`: Validates the ETL pipeline, table schemas, row counts, and foreign key join integrity.
* `tests/test_tools.py`: Tests catalog filtering, product lookups, PIX discount calculations, and order status retrieval.
* `tests/test_guardrails.py`: 16 test cases verifying deterministic interception of accessory inquiries and off-topic prompts, alongside passage of valid instrument requests.
* `tests/test_agent.py`: Validates the ReAct loop, tool dispatching, and multi-turn conversational memory.
* `tests/test_api.py`: Tests HTTP endpoints (`/api/health`, `/api/chat`, `/api/chat/history/{sessionId}`).
* `tests/test_frontend.py`: Integration tests for the React SPA (HTML structure, Artefact visual branding, LocalStorage keys).
* `tests/harness/test_harness.py`: Automated assertion runner executing ground-truth evaluations.

### 3.2. Evaluation Harness Benchmark Runner

```bash
python tests/harness/run_eval.py
```

Benchmark evaluation results:
* Total Test Cases: 10
* Passed Cases: 10 / 10 (100.0%)
* Guardrail Precision: 3 / 3 (100.0%)
* Tool Routing Accuracy: 7 / 7 (100.0%)
* Total Evaluation Time: 0.29 seconds

---

## 4. Sample Agent Interactions

Five representative end-to-end conversation flows are documented in [`examples/conversations.md`](examples/conversations.md):

1. **Catalog Search with Price Ceiling**: "Quais opções de violões disponíveis vocês têm custando até R$1000?" (Executes `search_products`).
2. **Specific Instrument Inquiry & Payment Conditions**: "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?" (Executes `get_product_details` and `get_store_policies`).
3. **Store Return Policy & Statutory Right of Withdrawal (CDC)**: "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido?" (Executes `get_store_policies`).
4. **Scope Guardrail Interception**: "Vocês vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?" (Zero-token interception with polite refusal and partner referral).
5. **Relational Order Tracking**: "Gostaria de saber o status do meu pedido 1. Quando chega?" (Executes `check_order_status`).

---

## 5. Known Limitations and Production Roadmap

1. **PostgreSQL Migration via Docker**:
   * *Current State*: Relational persistence in SQLite with foreign key enforcement and indexes.
   * *Production Plan*: Deploy a containerized PostgreSQL instance (`postgres:16-alpine`) managed via `docker-compose.yml`, supporting concurrent write scaling and connection pooling.
2. **Dense Vector Embeddings (Hybrid Search)**:
   * Introduce a vector store (`pgvector` or Qdrant) to support acoustic and stylistic similarity queries (e.g., "warm-sounding acoustic guitar for fingerstyle jazz").
3. **Production Observability and Tracing**:
   * Instrument the ReAct agent with OpenTelemetry or LangSmith for latency tracking, token usage attribution per session, and prompt drift detection.
4. **Omnichannel Messaging & Audio Processing**:
   * Integrate the WhatsApp Cloud API for multi-channel support and deploy Whisper for incoming voice note transcription.

---

## 6. Engineering Transparency Statement

In alignment with evaluation guidelines regarding the use of AI tools:
* **Tool Employed**: Antigravity AI Engineer (DeepMind / Gemini 3.8).
* **Workflow Methodology**:
  * Utilized as an engineering pair programmer to accelerate development velocity.
  * Accelerated the generation of Pydantic schemas, initial ETL data transformation scripts, unit test suites, and evaluation benchmark harness structures.
  * All architectural decisions (LangChain ReAct with LangGraph, deterministic pre-LLM scope guardrails, structured policy RAG, and relational database design) were designed, reviewed, and validated against challenge criteria.

---

## 7. Repository Directory Structure

```
artefact_ai_fullstack/
├── app/
│   ├── agent/
│   │   ├── guardrails.py       # Deterministic pre-LLM scope guardrails
│   │   ├── langchain_agent.py  # LangChain ReAct agent (LangGraph)
│   │   ├── memory.py           # Multi-turn conversation persistence
│   │   └── persona.py          # Store persona and prompt instructions
│   ├── api/
│   │   ├── routes.py           # FastAPI REST endpoints
│   │   └── server.py           # FastAPI application and static asset server
│   ├── db/
│   │   ├── database.py         # Relational database manager (SQLite)
│   │   └── etl.py              # ETL pipeline for raw operational CSV files
│   ├── knowledge/
│   │   └── policies.py         # RAG knowledge base extracted from policy PDF
│   ├── static/
│   │   └── index.html          # Responsive React SPA with Artefact visual identity
│   ├── tools/
│   │   ├── catalog_tools.py    # Catalog queries, price filters, and promotions
│   │   ├── langchain_tools.py  # LangChain tool definitions (@tool)
│   │   ├── order_tools.py      # Order tracking and customer purchase joins
│   │   └── policy_tools.py     # RAG policy retrieval tool
│   ├── config.py               # Environment configuration and settings
│   └── main.py                 # Uvicorn entry point
├── data/
│   ├── *.csv                   # Operational CSV files provided for the challenge
│   ├── políticas_da_loja.pdf   # Internal store policies and procedures manual
│   └── emporio.db              # Relational SQLite database generated by ETL
├── examples/
│   └── conversations.md        # Five documented interaction scenarios
├── frontend/                   # React TypeScript source files
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   └── types.ts
│   └── package.json
├── tests/
│   ├── harness/
│   │   ├── golden_dataset.json # Ground-truth evaluation dataset
│   │   ├── run_eval.py         # Standalone benchmark runner
│   │   └── test_harness.py     # Automated evaluation harness test suite
│   ├── test_agent.py           # Agent and memory tests
│   ├── test_api.py             # API route integration tests
│   ├── test_database.py        # Database integrity and ETL tests
│   ├── test_frontend.py        # Frontend integration and branding tests
│   ├── test_guardrails.py      # Guardrail unit and parametric tests
│   └── test_tools.py           # Business tools tests
├── .env.example
├── pyproject.toml
└── README.md
```
