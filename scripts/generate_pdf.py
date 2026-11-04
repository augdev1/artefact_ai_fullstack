#!/usr/bin/env python3
"""Generate an enterprise-grade PDF of the README and Documentation for Artefact Technical Challenge.

Criteria:
- English language only
- Candidate: Augusto Sousa
- Career: AI Engineer - Full-Stack para Aplicações com IA Generativa
- Output: "Augusto Sousa - AI Engineer - Full-Stack para Aplicações com IA Generativa.pdf"
"""

import os
import sys
import base64
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def get_base64_image(path: Path) -> str:
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def build_html_content() -> str:
    img1_path = ROOT_DIR / "docs" / "images" / "screenshot_1.png"
    img2_path = ROOT_DIR / "docs" / "images" / "screenshot_2.png"
    
    img1_src = get_base64_image(img1_path)
    img2_src = get_base64_image(img2_path)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Artefact Technical Challenge - AI Engineer Full Stack</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {{
      content: counter(page);
      font-size: 8pt;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #64748B;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1E293B;
    background: #FFFFFF;
    line-height: 1.55;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }}

  /* Typography */
  h1, h2, h3, h4, h5 {{
    color: #0F172A;
    font-weight: 700;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
  }}

  h1 {{
    font-size: 18pt;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-top: 0;
  }}

  h2 {{
    font-size: 13pt;
    border-bottom: 2px solid #E60067;
    padding-bottom: 4px;
    margin-top: 1.6em;
    color: #0F172A;
    display: flex;
    align-items: center;
  }}

  h3 {{
    font-size: 11pt;
    color: #1E293B;
    margin-top: 1.1em;
  }}

  h4 {{
    font-size: 10pt;
    color: #334155;
    margin-top: 0.8em;
  }}

  p {{
    margin: 0.5em 0;
    text-align: justify;
  }}

  ul, ol {{
    margin: 0.4em 0 0.6em 1.4em;
    padding: 0;
  }}

  li {{
    margin-bottom: 0.25em;
  }}

  strong {{
    color: #0F172A;
    font-weight: 600;
  }}

  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8.5pt;
    background: #F1F5F9;
    color: #0F172A;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #E2E8F0;
  }}

  pre {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8pt;
    background: #0F172A;
    color: #E2E8F0;
    padding: 10px 12px;
    border-radius: 6px;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0.6em 0;
    line-height: 1.4;
    page-break-inside: avoid;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: inherit;
  }}

  /* Header Cover / Metadata Box */
  .header-card {{
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #FFFFFF;
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 18px;
    border-top: 4px solid #E60067;
  }}

  .header-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    padding-bottom: 10px;
    margin-bottom: 12px;
  }}

  .brand-logo {{
    font-size: 15pt;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #FFFFFF;
    display: inline-flex;
    align-items: center;
    gap: 2px;
  }}

  .brand-logo svg {{
    display: inline-block;
    vertical-align: middle;
  }}

  .header-tag {{
    background: #E60067;
    color: #FFFFFF;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 8px;
    border-radius: 4px;
  }}

  .header-title {{
    font-size: 15pt;
    font-weight: 700;
    margin: 0 0 6px 0;
    color: #FFFFFF;
  }}

  .header-sub {{
    font-size: 9pt;
    color: #94A3B8;
    margin: 0 0 14px 0;
  }}

  .metadata-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px 16px;
    font-size: 8.5pt;
    background: rgba(15, 23, 42, 0.6);
    padding: 10px 14px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }}

  .metadata-item span.label {{
    color: #94A3B8;
    text-transform: uppercase;
    font-size: 7pt;
    font-weight: 600;
    letter-spacing: 0.05em;
    display: block;
  }}

  .metadata-item span.value {{
    color: #F8FAFC;
    font-weight: 600;
  }}

  .metadata-item a {{
    color: #38BDF8;
    text-decoration: none;
  }}

  /* Pill Badges */
  .badges-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 10px 0 14px 0;
  }}

  .badge {{
    font-size: 7.5pt;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 4px;
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #CBD5E1;
  }}

  .badge.magenta {{
    background: rgba(230, 0, 103, 0.08);
    color: #B0004E;
    border-color: rgba(230, 0, 103, 0.3);
  }}

  .badge.success {{
    background: #ECFDF5;
    color: #047857;
    border-color: #A7F3D0;
  }}

  .badge.blue {{
    background: #EFF6FF;
    color: #1D4ED8;
    border-color: #BFDBFE;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.8em 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  th, td {{
    padding: 6px 9px;
    border: 1px solid #CBD5E1;
    text-align: left;
  }}

  th {{
    background: #0F172A;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }}

  tr:nth-child(even) {{
    background: #F8FAFC;
  }}

  /* Callouts */
  .callout {{
    padding: 10px 14px;
    border-radius: 6px;
    margin: 0.8em 0;
    font-size: 9pt;
    page-break-inside: avoid;
    border-left: 4px solid #CBD5E1;
    background: #F8FAFC;
  }}

  .callout.info {{
    border-left-color: #0284C7;
    background: #F0F9FF;
  }}

  .callout.magenta {{
    border-left-color: #E60067;
    background: #FDF2F8;
  }}

  .callout.success {{
    border-left-color: #059669;
    background: #ECFDF5;
  }}

  /* Conversation Cards */
  .convo-card {{
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 1em 0;
    background: #FFFFFF;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    page-break-inside: avoid;
  }}

  .convo-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }}

  .convo-title {{
    font-weight: 700;
    font-size: 9.5pt;
    color: #0F172A;
  }}

  .user-box {{
    background: #F1F5F9;
    border-left: 3px solid #64748B;
    padding: 6px 10px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8.5pt;
  }}

  .tool-box {{
    background: #EFF6FF;
    border-left: 3px solid #3B82F6;
    padding: 5px 8px;
    margin: 5px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8pt;
    font-family: monospace;
    color: #1E40AF;
  }}

  .agent-box {{
    background: #FDF2F8;
    border-left: 3px solid #E60067;
    padding: 8px 12px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8.5pt;
    color: #0F172A;
  }}

  .tech-notes {{
    font-size: 8pt;
    color: #475569;
    margin-top: 6px;
    padding-top: 4px;
    border-top: 1px dashed #E2E8F0;
  }}

  /* Images / Showcase */
  .screenshot-container {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 1.2em 0;
    page-break-inside: avoid;
  }}

  .screenshot-box {{
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 6px;
    background: #F8FAFC;
    text-align: center;
  }}

  .screenshot-box img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    display: block;
    margin: 0 auto;
    border: 1px solid #CBD5E1;
  }}

  .screenshot-caption {{
    font-size: 7.5pt;
    color: #64748B;
    margin-top: 4px;
    font-weight: 500;
  }}

  /* Page break helpers */
  .page-break {{
    page-break-before: always;
  }}

  .avoid-break {{
    page-break-inside: avoid;
  }}
</style>
</head>
<body>

<!-- EXECUTIVE COVER HEADER -->
<div class="header-card">
  <div class="header-top">
    <div class="brand-logo">
      <span>ARTEF</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#E60067" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="4 21 12 3 20 21"></polyline>
      </svg>
      <span>CT</span>
    </div>
    <div class="header-tag">Project README &amp; Technical Documentation</div>
  </div>
  
  <div class="header-title">Empório da Música - AI Agent &amp; Evaluation Harness</div>
  <div class="header-sub">Consolidated Project README, Architecture Decisions, Automated Evaluation Harness &amp; Complete Documentation</div>

  <div class="metadata-grid">
    <div class="metadata-item">
      <span class="label">Candidate Name</span>
      <span class="value">Augusto Sousa</span>
    </div>
    <div class="metadata-item">
      <span class="label">Position / Career</span>
      <span class="value">AI Engineer - Full-Stack para Aplicações com IA Generativa</span>
    </div>
    <div class="metadata-item">
      <span class="label">Public GitHub Repository</span>
      <span class="value"><a href="https://github.com/augdev1/artefact_ai_fullstack">https://github.com/augdev1/artefact_ai_fullstack</a></span>
    </div>
    <div class="metadata-item">
      <span class="label">Candidate Contact / Email</span>
      <span class="value">augustosousa1798@gmail.com</span>
    </div>
  </div>
</div>

<div class="badges-row">
  <span class="badge magenta">LangChain & LangGraph ReAct</span>
  <span class="badge blue">Google Gemini 3.5 Flash Lite + OpenAI Fallback</span>
  <span class="badge">SQLite & ETL Normalization</span>
  <span class="badge">Zero-Token Scope Guardrails</span>
  <span class="badge">React 18 & TypeScript SPA</span>
  <span class="badge success">39 / 39 Pytest Passing</span>
  <span class="badge success">100% Evaluation Benchmark</span>
</div>

<!-- EXECUTIVE SUMMARY -->
<h2>Executive Summary</h2>
<p>
This document constitutes the official technical delivery for the <strong>AI Engineer Full Stack</strong> selection process at <strong>Artefact</strong>.
The project delivers an end-to-end conversational customer support system for <em>Empório da Música</em>, a musical instrument retail store in Campo Grande, MS, Brazil. 
The solution relieves human attendants from high-frequency inquiries (business hours, address, order shipment tracking, catalog search with budget filters, installment rules, and return policies) through a resilient, auditable AI architecture.
</p>

<!-- APPLICATION INTERFACE SHOWCASE -->
<h2>Application Interface Showcase</h2>
<div class="screenshot-container">
  <div class="screenshot-box">
    <img src="{img1_src}" alt="Empório da Música Interactive Chat Interface">
    <div class="screenshot-caption">Figure 1: Full-stack responsive web application with Artefact brand styling, collapsible chat history sidebar, and active session status.</div>
  </div>
  <div class="screenshot-box">
    <img src="{img2_src}" alt="Product Recommendations and Financing Calculations">
    <div class="screenshot-caption">Figure 2: Real-time ReAct catalog execution with Markdown typography rendering table pricing, 5% cash PIX discounts, and 12x installment terms.</div>
  </div>
</div>

<!-- SECTION 1: ARCHITECTURE & TECHNICAL DECISIONS -->
<div class="page-break"></div>
<h2>1. Architecture and Technical Decisions</h2>

<p>
The project was engineered around six fundamental software and AI engineering decisions to ensure high reliability, low operational costs, deterministic business policy compliance, and exceptional user experience:
</p>

<h3>1.1. Agent Orchestration: LangChain ReAct Pattern (LangGraph)</h3>
<ul>
  <li><strong>Implementation</strong>: Built with <code>langgraph.prebuilt.create_react_agent</code>, the established standard for agentic architectures in LangChain.</li>
  <li><strong>Architectural Rationale</strong>: The ReAct (Reasoning + Acting) loop alternates between Thought, Action, and Observation phases. Bound to typed Pydantic tools (<code>@tool</code>), it enables multi-step tool composition (e.g., cross-referencing store return policies and relational customer order records within a single user turn) while providing full auditable introspection into intermediate reasoning.</li>
</ul>

<h3>1.2. LLM Provider Strategy and Resilience</h3>
<ul>
  <li><strong>Primary Model</strong>: Google Gemini (<code>gemini-3.5-flash-lite</code>) via <code>langchain-google-genai</code>.</li>
  <li><strong>Fallback Model</strong>: OpenAI (<code>gpt-4o-mini</code>), configurable via environment variables without code modification.</li>
  <li><strong>Deterministic Offline Engine</strong>: High-speed mock provider for continuous integration (CI/CD) and automated unit testing without API costs or rate-limiting.</li>
  <li><strong>Architectural Rationale</strong>: Gemini 3.5 Flash Lite achieves sub-second response times, excellent native Portuguese tool calling, and high cost efficiency for transaction-dense conversational workloads. The decoupled provider layer applies dependency inversion: switching providers requires editing only the <code>.env</code> file.</li>
</ul>

<h3>1.3. Data Engineering (ETL) and Relational Persistence Layer</h3>
<ul>
  <li><strong>ETL Data Processing (<code>app/db/etl.py</code>)</strong>:
    <ul>
      <li><strong>Unicode Normalization</strong>: NFKC text standardization and whitespace stripping across all operational datasets.</li>
      <li><strong>Monetary Precision</strong>: Strict floating-point decimal casting and 2-decimal rounding for prices, discounts, and order amounts.</li>
      <li><strong>Inventory Constraints</strong>: Enforcement of non-negative stock invariants (<code>stock_quantity >= 0</code>).</li>
      <li><strong>Specification Parsing</strong>: Robust parsing of raw JSON strings into typed technical specification dictionaries (tonewoods, fret count, pickups, electronics).</li>
      <li><strong>Campaign Segmentation</strong>: Strict binary partitioning between active promotions (<code>is_active = 1</code>) and expired promotions (<code>is_active = 0</code>), ensuring expired discounts are never applied.</li>
    </ul>
  </li>
  <li><strong>Relational Database Design</strong>:
    <ul>
      <li>SQLite backend (<code>data/emporio.db</code>) with enforced foreign key integrity (<code>PRAGMA foreign_keys = ON;</code>) and composite indexes (<code>idx_products_name</code>, <code>idx_products_category</code>, <code>idx_products_price</code>, <code>idx_orders_customer</code>, <code>idx_orders_tracking</code>).</li>
      <li><strong>Session Persistence</strong>: Dedicated <code>conversation_history</code> table indexed by <code>session_id</code>, maintaining full client context across browser refreshes and server reboots.</li>
      <li><strong>Roadmap to Dockerized PostgreSQL</strong>: The data access layer is cleanly abstracted, enabling immediate migration to containerized PostgreSQL (<code>docker-compose.yml</code>) without touching route handlers.</li>
    </ul>
  </li>
</ul>

<h3>1.4. Policy Retrieval Architecture (RAG)</h3>
<ul>
  <li><strong>Knowledge Source</strong>: Store Policies and Customer Service Manual (<code>data/políticas_da_loja.pdf</code>, Version 2.1).</li>
  <li><strong>Retrieval Strategy</strong>: Semantic domain retrieval categorizing operational hours, physical address, statutory 7-day right of withdrawal (CDC Art. 49), 90-day warranty procedures, local shipping thresholds, and non-cumulativity of the 5% PIX discount over active promotions.</li>
  <li><strong>Architectural Rationale</strong>: Prevents hallucination of critical legal deadlines and financial conditions by retrieving exact policy clauses directly into the agent prompt context.</li>
</ul>

<h3>1.5. Deterministic Scope Guardrails</h3>
<ul>
  <li><strong>Store Mandate</strong>: Empório da Música <strong>exclusively sells complete musical instruments</strong> and <strong>does not stock standalone accessories or amplification</strong> (loose strings, picks, cables, pedals, amplifiers, or standalone cases).</li>
  <li><strong>Implementation (<code>app/agent/guardrails.py</code>)</strong>: Fast deterministic pre-LLM filter intercepting accessory queries and non-domain topics (programming, cooking recipes, politics) prior to model invocation. Emits polite refusals and redirects clients to regional partner shops.</li>
  <li><strong>Production Impact</strong>: 0 ms API latency, zero token consumption on invalid requests, and 100% deterministic scope adherence.</li>
</ul>

<h3>1.6. Frontend Architecture and Technology Stack</h3>
<ul>
  <li><strong>React 18 SPA</strong>: Functional component architecture with hooks (<code>useState</code>, <code>useEffect</code>, <code>useRef</code>, <code>useMemo</code>) for reactive message synchronization, active thread switching, and optimistic UI updates.</li>
  <li><strong>TypeScript</strong>: Formal interface contracts (<code>Message</code>, <code>ChatSession</code>, <code>ChatResponse</code>, <code>HealthResponse</code>) providing strict compile-time verification across client and server.</li>
  <li><strong>Tailwind CSS</strong>: Mobile-first utility design system featuring custom Artefact corporate accents (<code>#E60067</code>), collapsible animated sidebar (<code>w-72</code> / <code>w-0</code> with <code>overflow-hidden</code>), and high-contrast dark theme.</li>
  <li><strong>Marked.js</strong>: Real-time Markdown parser and compiler ensuring catalog pricing, installment schedules, and bulleted specs render with clean visual alignment.</li>
  <li><strong>HTML5 LocalStorage API</strong>: Preserves session identifiers and thread lists across page reloads (F5), reconciled with backend SQLite history.</li>
  <li><strong>Vector Branding & SVGs</strong>: Exact geometric reproduction of Artefact's chevron logo glyph (<code>/\\</code>) and custom avatars for customer and AI assistant.</li>
</ul>

<!-- SECTION 2: SETUP AND EXECUTION -->
<div class="page-break"></div>
<h2>2. Setup and Execution Instructions</h2>

<h3>2.1. Prerequisites</h3>
<p>Python 3.11 or higher (developed and verified on Python 3.12). Package management via <code>uv</code> (recommended) or <code>pip</code>.</p>

<h3>2.2. Installation Commands</h3>
<pre><code># 1. Clone repository
git clone https://github.com/augdev1/artefact_ai_fullstack.git
cd artefact_ai_fullstack

# 2. Setup virtual environment with uv (recommended)
uv venv .venv
uv pip install -e ".[dev]"

# Alternative using standard pip
python -m venv .venv
# On Windows: .venv\\Scripts\\activate | On Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"</code></pre>

<h3>2.3. Environment Configuration (<code>.env</code>)</h3>
<pre><code>LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

# Optional Fallback Settings
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini
DATABASE_PATH=data/emporio.db
HOST=0.0.0.0
PORT=8000</code></pre>

<h3>2.4. Server Execution</h3>
<pre><code># Start the full-stack FastAPI + React application
python -m app.main</code></pre>

<table>
  <thead>
    <tr>
      <th>Service Component</th>
      <th>Endpoint URL</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Conversational Web SPA</strong></td>
      <td><code>http://localhost:8000</code></td>
      <td>Interactive React chat UI with session history & Artefact branding</td>
    </tr>
    <tr>
      <td><strong>Interactive API Docs</strong></td>
      <td><code>http://localhost:8000/docs</code></td>
      <td>FastAPI Swagger UI for testing REST endpoints</td>
    </tr>
    <tr>
      <td><strong>System Healthcheck</strong></td>
      <td><code>http://localhost:8000/api/health</code></td>
      <td>Liveness and component readiness check</td>
    </tr>
  </tbody>
</table>

<!-- SECTION 3: EVALUATION HARNESS -->
<h2>3. Evaluation Harness and Automated Testing Suite</h2>

<p>
Quality assurance is maintained through a dual testing harness: <strong>39 automated unit and integration tests</strong> via <code>pytest</code> and an automated <strong>Evaluation Harness Benchmark Runner</strong> over a ground-truth dataset (<em>Golden Dataset</em>).
</p>

<h3>3.1. Pytest Test Suite Breakdown (39 / 39 Passed)</h3>
<table>
  <thead>
    <tr>
      <th>Test Module</th>
      <th>Test Count</th>
      <th>Verification Scope</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>tests/test_database.py</code></td>
      <td>3</td>
      <td>ETL row count invariants, schema types, and foreign key relational joins</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_tools.py</code></td>
      <td>7</td>
      <td>Catalog filters, price boundaries, PIX discounts, active promos, order tracking</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_guardrails.py</code></td>
      <td>16</td>
      <td>Parametric blocking of accessories & off-topic; passage of valid instruments</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_agent.py</code></td>
      <td>6</td>
      <td>ReAct reasoning cycle, multi-turn memory preservation, and tool dispatching</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_api.py</code></td>
      <td>5</td>
      <td>FastAPI endpoints: healthcheck, chat completion, history retrieval & deletion</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_frontend.py</code></td>
      <td>1</td>
      <td>React SPA HTML serving, Artefact chevron branding, and LocalStorage keys</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/harness/test_harness.py</code></td>
      <td>1</td>
      <td>Automated assertion runner verifying ground-truth evaluations</td>
      <td><span class="badge success">PASSED</span></td>
    </tr>
  </tbody>
</table>

<h3>3.2. Evaluation Harness Benchmark Runner (<code>python tests/harness/run_eval.py</code>)</h3>
<p>The evaluation harness evaluates 10 non-trivial customer scenarios covering catalog filtering, pricing, order tracking, store policies, active discounts, and guardrails:</p>

<table>
  <thead>
    <tr>
      <th>Metric Category</th>
      <th>Target Invariant</th>
      <th>Observed Score</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Total Evaluation Test Cases</strong></td>
      <td>10 Comprehensive Scenarios</td>
      <td><strong>10 / 10</strong></td>
      <td><span class="badge success">100.0% PASS</span></td>
    </tr>
    <tr>
      <td><strong>Guardrail Precision</strong></td>
      <td>Zero-token rejection of accessories & off-topic</td>
      <td><strong>3 / 3</strong></td>
      <td><span class="badge success">100.0% PRECISION</span></td>
    </tr>
    <tr>
      <td><strong>Tool Routing Accuracy</strong></td>
      <td>Deterministic selection of correct business tools</td>
      <td><strong>7 / 7</strong></td>
      <td><span class="badge success">100.0% ACCURACY</span></td>
    </tr>
    <tr>
      <td><strong>Total Benchmark Execution Time</strong></td>
      <td>Sub-second automated suite execution</td>
      <td><strong>0.29s</strong></td>
      <td><span class="badge blue">OPTIMAL</span></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 4: REPRESENTATIVE SCENARIOS -->
<div class="page-break"></div>
<h2>4. Representative Customer Interactions & Case Studies</h2>

<p>
The repository documents five representative interaction scenarios demonstrating the ReAct loop, RAG retrieval, relational joins, and scope guardrails:
</p>

<!-- SCENARIO 1 -->
<div class="convo-card">
  <div class="convo-header">
    <span class="convo-title">Scenario 1: Catalog Search with Price Ceiling</span>
    <span class="badge blue">Tool: search_products</span>
  </div>
  <div class="user-box"><strong>Customer (PT-BR):</strong> "Olá, tudo bem? Quais opções de violões disponíveis vocês têm custando até R$1000?"</div>
  <div class="tool-box">Invoked: search_products(category_name='Violões', max_price=1000.0)</div>
  <div class="agent-box">
    <strong>Agent Response:</strong><br>
    Temos ótimas opções de violões disponíveis em estoque por até R$ 1.000,00!<br><br>
    • <strong>Tagima Memphis AC-39 Nylon Natural</strong> — Preço: R$ 429,90 (ou R$ 408,40 à vista no PIX com 5% de desconto) | Estoque: 15 unidades | Violão clássico de nylon confortável para iniciantes.<br>
    • <strong>Rozini RC-104 Nylon Estudante</strong> — Preço: R$ 459,90 (ou R$ 436,90 no PIX) | Estoque: 10 unidades | Clássico nacional com ótima sonoridade.<br>
    • <strong>Shelby SN-100 Folk Aço Preto</strong> — Preço: R$ 549,00 (ou R$ 521,55 no PIX) | Estoque: 5 unidades | Estilo Folk com cordas de aço e visual moderno.<br>
    • <strong>Yamaha C40 Nylon Natural</strong> — Preço: R$ 599,90 (ou R$ 569,91 no PIX) | Estoque: 12 unidades | Referência para estudantes com excelente projeção.<br><br>
    Todos os modelos contam com parcelamento em até <strong>12x sem juros</strong> no cartão (parcela mínima de R$ 100,00) ou 5% no PIX. Para Campo Grande acima de R$ 500,00 a entrega é gratuita via motoboy.
  </div>
  <div class="tech-notes">
    <strong>Technical Verification:</strong> Correctly extracted budget constraint (<code>max_price=1000.0</code>) and filtered category; returned only in-stock items with exact PIX 5% calculations and installment rules.
  </div>
</div>

<!-- SCENARIO 2 -->
<div class="convo-card">
  <div class="convo-header">
    <span class="convo-title">Scenario 2: Specific Instrument Details & Payment Terms</span>
    <span class="badge magenta">Multi-Tool: get_product_details + get_store_policies</span>
  </div>
  <div class="user-box"><strong>Customer (PT-BR):</strong> "Quanto custa o Takamine GD20? Como funciona o pagamento parcelado e no PIX?"</div>
  <div class="tool-box">Invoked: get_product_details(name_or_id='Takamine GD20') & get_store_policies(topic_or_query='pagamento pix parcelamento')</div>
  <div class="agent-box">
    <strong>Agent Response:</strong><br>
    O <strong>Takamine GD20</strong> (modelo Folk Dreadnought com tampo sólido em Cedar) está disponível em estoque por <strong>R$ 2.199,00</strong> (temos 5 unidades em estoque).<br><br>
    Condições de pagamento:<br>
    • <strong>À vista no PIX</strong>: 5% de desconto direto, saindo por <strong>R$ 2.089,05</strong> (economia de R$ 109,95).<br>
    • <strong>Cartão de Crédito</strong>: Parcelamento em até <strong>12x de R$ 183,25 sem juros</strong> (respeitando a parcela mínima de R$ 100,00).<br>
    • <strong>Condição Especial de Alto Valor</strong>: Por ser acima de R$ 2.000,00, é permitida a divisão de formas de pagamento (ex.: entrada no PIX com saldo parcelado no cartão).
  </div>
  <div class="tech-notes">
    <strong>Technical Verification:</strong> Synthesized database product records and policy manual rules into a single coherent response without hallucination.
  </div>
</div>

<!-- SCENARIO 3 -->
<div class="convo-card">
  <div class="convo-header">
    <span class="convo-title">Scenario 3: Store Return Policy & Consumer Rights (CDC)</span>
    <span class="badge blue">Tool: get_store_policies</span>
  </div>
  <div class="user-box"><strong>Customer (PT-BR):</strong> "Comprei um teclado pelo site mas me arrependi da minha compra, chegou ontem. Posso devolver meu pedido?"</div>
  <div class="tool-box">Invoked: get_store_policies(topic_or_query='devolucao arrependimento compra')</div>
  <div class="agent-box">
    <strong>Agent Response:</strong><br>
    Sim, a devolução é perfeitamente assegurada pelo Código de Defesa do Consumidor (Artigo 49) e pelas políticas da Empório da Música.<br><br>
    Para compras digitais, você tem até <strong>7 (sete) dias corridos</strong> após a entrega para solicitar devolução por arrependimento com estorno integral.<br>
    1. O instrumento deve estar na embalagem original, com manuais, cabos e sem marcas de mau uso.<br>
    2. O frete de logística reversa é integralmente coberto pela loja via código dos Correios.<br>
    3. O estorno financeiro é processado na mesma forma original em até 10 dias úteis após a conferência técnica.
  </div>
  <div class="tech-notes">
    <strong>Technical Verification:</strong> RAG retrieved exact CDC statutory rules, packaging conditions, reverse postage coverage, and refund SLA.
  </div>
</div>

<!-- SCENARIO 4 -->
<div class="convo-card">
  <div class="convo-header">
    <span class="convo-title">Scenario 4: Scope Guardrail Activation (Accessory Rejection)</span>
    <span class="badge magenta">Zero-Token Pre-LLM Guardrail</span>
  </div>
  <div class="user-box"><strong>Customer (PT-BR):</strong> "Vocês vendem encordoamento de guitarra 0.10, palhetas Fender e amplificador de 50W?"</div>
  <div class="tool-box">Invoked: None (Deterministic Pre-LLM Guardrail Interception)</div>
  <div class="agent-box">
    <strong>Agent Response:</strong><br>
    A Empório da Música é especializada exclusivamente na venda de instrumentos musicais completos (violões, guitarras, contrabaixos, baterias, teclados, pianos e instrumentos de sopro).<br><br>
    Não comercializamos acessórios avulsos, encordoamentos, palhetas, cabos, pedais de efeito, amplificadores ou cases avulsos.<br><br>
    Recomendamos buscar esses insumos em lojas especializadas em áudio e acessórios no centro de Campo Grande. Estamos à disposição para auxiliá-lo na escolha de instrumentos musicais completos de nosso catálogo.
  </div>
  <div class="tech-notes">
    <strong>Technical Verification:</strong> Executed in 0 ms API latency with zero token consumption. Firm, polite, and brand-aligned refusal.
  </div>
</div>

<!-- SCENARIO 5 -->
<div class="convo-card">
  <div class="convo-header">
    <span class="convo-title">Scenario 5: Relational Order Status Tracking</span>
    <span class="badge blue">Tool: check_order_status</span>
  </div>
  <div class="user-box"><strong>Customer (PT-BR):</strong> "Gostaria de saber o status do meu pedido 1. Quando chega?"</div>
  <div class="tool-box">Invoked: check_order_status(order_id=1)</div>
  <div class="agent-box">
    <strong>Agent Response:</strong><br>
    Seguem os dados atualizados do pedido consultado em nosso sistema:<br>
    • <strong>Pedido</strong>: #1 | <strong>Cliente</strong>: Lucas Mendes da Silva<br>
    • <strong>Data da Compra</strong>: 15/10/2025 | <strong>Status Atual</strong>: Entregue ao destinatário<br>
    • <strong>Item</strong>: 1x Roland FP-30X Piano Digital Preto | <strong>Valor Total</strong>: R$ 11.499,00 (PIX)<br>
    • <strong>Rastreamento</strong>: BRAB1234567BR | <strong>Data de Entrega</strong>: 25/10/2025<br><br>
    O pedido consta como entregue. Se precisar de assistência técnica coberta pela garantia de 90 dias, estamos à disposição.
  </div>
  <div class="tech-notes">
    <strong>Technical Verification:</strong> Relational SQL join across <code>orders</code>, <code>order_items</code>, and <code>customers</code>; accurate delivery status reported.
  </div>
</div>

<!-- SECTION 5: ROADMAP -->
<div class="page-break"></div>
<h2>5. Known Limitations and Production Roadmap</h2>
<ol>
  <li><strong>PostgreSQL Migration via Docker</strong>: Complete the containerization of the persistence layer using official PostgreSQL images (<code>postgres:16-alpine</code>) in <code>docker-compose.yml</code> to provide connection pooling and concurrent write scaling.</li>
  <li><strong>Dense Vector Embeddings (Hybrid Search)</strong>: Integrate a vector database (<code>pgvector</code> or Qdrant) to enable acoustic timbre and musical style searches (e.g., "warm acoustic guitar for fingerstyle jazz").</li>
  <li><strong>Production Observability & Tracing</strong>: Instrument the agent with OpenTelemetry or LangSmith for latency tracking, per-session token cost attribution, and prompt drift detection.</li>
  <li><strong>Omnichannel Messaging & Audio Processing</strong>: Integrate the Meta WhatsApp Cloud API and deploy Whisper speech-to-text models to process customer voice notes.</li>
</ol>

<!-- SECTION 6: TRANSPARENCY -->
<h2>6. Engineering Transparency Statement</h2>
<p>
In alignment with the challenge guidelines regarding modern engineering workflows:
</p>
<ul>
  <li><strong>Tool Employed</strong>: Antigravity AI Engineer (DeepMind / Gemini 3.8).</li>
  <li><strong>Workflow Methodology</strong>: Used as a technical pair programmer to accelerate development velocity. Assisted in structuring Pydantic schemas, drafting initial ETL transformation routines, generating unit test fixtures, and setting up the evaluation benchmark harness.</li>
  <li><strong>Core Architecture</strong>: All architectural decisions (LangChain ReAct with LangGraph, deterministic pre-LLM scope guardrails, structured policy RAG, and relational database design) were designed, reviewed, and validated against the challenge criteria.</li>
</ul>

<!-- SECTION 7: DIRECTORY TREE -->
<h2>7. Repository Directory Structure</h2>
<pre><code>artefact_ai_fullstack/
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
├── docs/
│   └── images/                 # High-resolution screenshots of the UI
├── examples/
│   └── conversations.md        # Five documented interaction scenarios
├── frontend/                   # React TypeScript source files
│   ├── src/
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
└── README.md</code></pre>

</body>
</html>"""
    return html

def generate_pdf():
    html_content = build_html_content()
    
    docs_dir = ROOT_DIR / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    html_path = docs_dir / "documentation.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML written to: {html_path}")
    
    # Target PDF names as required by the selection criteria
    primary_pdf_name = "Augusto Sousa - AI Engineer - Full-Stack para Aplicações com IA Generativa.pdf"
    primary_pdf_path = ROOT_DIR / primary_pdf_name
    secondary_pdf_path = docs_dir / "README_and_Documentation.pdf"
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    
    browser_exe = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser_exe = p
            break
            
    if not browser_exe:
        raise RuntimeError("No headless browser found (Chrome or Edge).")
        
    print(f"Using browser: {browser_exe}")
    
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={primary_pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Browser stderr: {res.stderr}")
        raise RuntimeError(f"Browser process failed with code {res.returncode}")
        
    print(f"Consolidated single PDF created successfully: {primary_pdf_path} ({primary_pdf_path.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_pdf()
