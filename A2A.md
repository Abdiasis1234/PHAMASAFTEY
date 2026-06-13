# PhamaSafety — A2A Track

PhamaSafety is a **pharmaceutical safety tri-agent system** for the [Google A2A Hackathon](https://hackathon.a2anet.com), built on the [A2A hackathon template](https://github.com/a2anet/a2a-hackathon-template) and scored by the [a2a-hackathon harness](https://github.com/a2anet/a2a-hackathon).

The CopilotKit **Generative UI** demo (`/fixed`, `/dynamic`) runs in parallel as Track 2.

## Architecture

| Agent | Port | Role |
|-------|------|------|
| **Personal Agent** | `:9001` | Intake — extracts structured safety case fields, user-side env tools, contacts CS via A2A |
| **CS Agent** | `:9002` | Policy, verification, env tools, Redis KB search, orchestrates research |
| **Research Agent** | internal | BM25 + vector KB search inside the CS agent (`ask_research_agent`) |
| **redis** | `:6379` | Knowledge-base index (698 harness docs + 8 pharma safety docs) |

## Quick start

### 1. Configure

```powershell
copy .env.example .env
# Set GOOGLE_API_KEY / GEMINI_API_KEY (Vertex express key AQ.* or AI Studio key)
# GOOGLE_GENAI_USE_VERTEXAI=true
```

If your org blocks API keys, use ADC instead — see `scripts/setup-adc.ps1`.

### 2. Run A2A agents (requires Docker)

```powershell
docker compose up --build
```

### 3. Run Generative UI (optional Track 2)

```powershell
# Terminal 1 — LangGraph agents
cd agent
uv run uvicorn main:app --port 8123

# Terminal 2 — Next.js
npx next dev -p 3001
```

Open http://localhost:3001 — case intake at `/fixed`, follow-up Q&A at `/dynamic`.

### 4. Smoke test (harness)

Clone the harness repo beside this one, then:

```powershell
uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002
```

## Harness compatibility

The KB includes the full **698-document harness corpus** from the template plus **8 pharma safety documents** in `kb/documents/doc_pharma_*.json`. Agent prompts are customized for pharmaceutical safety cases while preserving harness tool names and compose shape.

## Compose services

- `personal-agent` → `:9001`
- `cs-agent` → `:9002` (runs KB ingest on startup)
- `redis` → `:6379`

When running standalone `docker compose up`, the personal agent uses `CS_AGENT_URL=http://cs-agent:9002`. When running the harness, set `CS_AGENT_URL=http://host.docker.internal:8090/cs-agent` in `.env`.
