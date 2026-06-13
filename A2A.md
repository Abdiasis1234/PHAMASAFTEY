# A2A Hackathon Track

This repo is configured for the **[A2A Interoperability Challenge](https://github.com/a2anet/a2a-hackathon-template)** (Track 1) — a two-agent Rho-Bank system scored by the [a2a-hackathon harness](https://github.com/a2anet/a2a-hackathon).

The CopilotKit **Generative UI** demo (`/fixed`, `/dynamic`) remains in the repo as optional Track 2 scaffolding but is **not** the primary dev loop for this track.

## Architecture

| Agent | Port | Role |
|-------|------|------|
| **personal-agent** | `:9001` | User's banking assistant — user-side env tools, contacts CS via A2A |
| **cs-agent** | `:9002` | Bank customer service — bank-side env tools, Redis KB (BM25 + vector) |
| **redis** | `:6379` | Knowledge-base index (698 documents) |

## Quick start

### 1. Configure

```powershell
copy .env.example .env
# Set GOOGLE_API_KEY (Vertex AI key from your GCP project)
```

### 2. Run agents

```powershell
docker compose up --build
```

### 3. Clone the harness (once, beside this repo)

```powershell
cd ..
git clone https://github.com/a2anet/a2a-hackathon.git
cd a2a-hackathon
uv sync
```

### 4. Smoke test

From the **harness** repo (with the same `GOOGLE_API_KEY` exported):

```powershell
$env:GOOGLE_API_KEY = "your-key"
uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002
```

`smoke` starts the env API on `:8090`, runs one simulated task, prints both conversation legs, every tool call, and the reward.

### 5. Train split

```powershell
uv run a2a-hack run --personal-url http://localhost:9001 --cs-url http://localhost:9002 `
  --tasks train --save-to results/dev --auto-resume
uv run tau2 view results/dev
```

## Submission rules (summary)

From the [official template](https://github.com/a2anet/a2a-hackathon-template):

- **Model:** `gemini-3.5-flash` (required for marked runs)
- **Compose shape:** `personal-agent`, `cs-agent`, `redis` — do not rename
- **contextId:** reuse on every env tool call and every personal→CS A2A message
- **Submit:** public GitHub repo + API key at [hackathon.a2anet.com](https://hackathon.a2anet.com)

## What's where

```
personal_agent/   Personal banking assistant (A2A :9001)
cs_agent/         Customer service + Redis RAG (A2A :9002)
kb/               policy.md + documents/ (698 JSON docs)
docker-compose.yml
agent/            Optional LangGraph A2UI agents (:8123) — Track 2
src/              Optional Next.js UI — Track 2
```

## Optional: precompute embeddings

Speeds CS agent startup (requires `GOOGLE_API_KEY`):

```powershell
cd cs_agent
$env:KB_DOCUMENTS_DIR = "..\kb\documents"
$env:KB_EMBEDDINGS_PATH = "..\kb\embeddings.json"
python precompute_embeddings.py
```

Without `kb/embeddings.json`, BM25 search still works; vector search embeds on first query when credentials are available.

## References

- [a2a-hackathon-template](https://github.com/a2anet/a2a-hackathon-template) — agent contract
- [a2a-hackathon](https://github.com/a2anet/a2a-hackathon) — harness CLI
- [A2A Net Discord](https://a2anet.com/) — community
