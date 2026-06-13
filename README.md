# Pharma Safety Tri-Agent System

A multi-agent customer support and research system built for the [Google A2A Hackathon](https://hackathon.a2anet.com), based on the [A2A Hackathon Template](https://github.com/a2anet/a2a-hackathon-template).

This project explores how three specialised agents can communicate over the Agent-to-Agent protocol to handle pharmaceutical safety reports — adverse drug reactions, missing patient details, medicine-related complaints, and regulatory escalation cases.

## Problem

Pharmaceutical companies receive large volumes of safety-related messages from patients, doctors, pharmacists, and support teams. These reports are often incomplete, emotional, or unstructured. In regulated environments, missing details can delay escalation, risk patient safety, and create compliance issues.

## Solution

Three cooperating agents transform an unstructured message into a structured safety case, research medical and regulatory context, and recommend the correct next action:

| Agent | Service | Role |
|-------|---------|------|
| **Personal Agent** | `:9001` (A2A) | Receives the customer message, extracts structured case fields, acts with user-side tools, contacts CS |
| **Customer Service Agent** | `:9002` (A2A) | Handles policy, verification, env tools, and orchestrates research |
| **Research Agent** | Internal to CS agent | Searches the KB (BM25 + vector), synthesises findings and escalation guidance |

The hackathon requires exactly two A2A services (`personal-agent`, `cs-agent`, `redis`). The Research Agent runs **inside** the CS agent container as an internal ADK agent invoked via `ask_research_agent`.

### Example structured case (Personal Agent → CS Agent)

```json
{
  "case_type": "adverse_drug_reaction",
  "medicine": "ExampleMed",
  "symptoms": ["dizziness", "nausea"],
  "severity": "moderate",
  "missing_fields": ["dosage", "patient_age"],
  "urgency": "high",
  "summary": "Patient reports dizziness and nausea after taking ExampleMed."
}
```

## Architecture

```text
Simulated user ──A2A──► Personal Agent (:9001)
                              │
                              │ ask_customer_service (A2A, same contextId)
                              ▼
                         CS Agent (:9002)
                              │
                              ├── ask_research_agent ──► Research Agent (internal)
                              │                               └── kb_search_bm25 / vector
                              ├── env tools (harness API)
                              └── Redis RAG index ◄── kb/documents
```

## Setup

### 1. Knowledge base

Copy `kb/documents/` from the [hackathon template](https://github.com/a2anet/a2a-hackathon-template/tree/main/kb/documents) — see `kb/documents/README.md`.

### 2. Configure

```powershell
cp .env.example .env
# Set GOOGLE_API_KEY (Vertex AI key from GCP)
```

### 3. Run agents

```powershell
docker compose up --build
```

### 4. Smoke test (requires [a2a-hackathon](https://github.com/a2anet/a2a-hackathon) CLI cloned nearby)

```powershell
uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002
```

## Hackathon rules (unchanged)

- Both A2A agents use **`gemini-3.5-flash`**; vector search uses `gemini-embedding-001`.
- Compose shape: `personal-agent` (`:9001`), `cs-agent` (`:9002`), `redis`.
- Reuse incoming **`contextId`** on every env tool call and every personal→CS A2A message.
- Fetch tools from the harness env API — do not hardcode them.
- Each agent turn ≤ 5 min; whole task ≤ 10 min.

See the [template README](https://github.com/a2anet/a2a-hackathon-template) for full rules, dev loop, and submission details.

## Generative UI (Track 2)

The same repo includes a **CopilotKit + A2UI** frontend for pharmaceutical safety case intake:

| Route | What it does |
|-------|----------------|
| `/` | PhamaSafety overview and tri-agent architecture |
| `/fixed` | Case intake chat → structured safety-case dashboard (A2UI) |
| `/dynamic` | Follow-up Q&A with dynamic charts and callouts |

```powershell
pnpm install
pnpm dev
# Or separately: Next.js on :3000 and LangGraph on :8123
```

Set `GEMINI_API_KEY` in `.env` for live LLM calls, or `OFFLINE=1` for a keyless fixed-dashboard demo.

## What's where

```
personal_agent/  agent.py (intake prompt), env_toolset.py, cs_client_tool.py, main.py
cs_agent/        agent.py (CS prompt), research_agent.py, research_tool.py,
                 env_toolset.py, rag_tools.py, ingest.py, main.py
kb/              policy.md + documents/ (copy from template)
```

## Submission

Submit your public repo URL and Vertex API key at [hackathon.a2anet.com](https://hackathon.a2anet.com).
