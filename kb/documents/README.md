# Knowledge base

Documents are JSON files in this folder (`id`, `title`, `content`).

- **698 harness documents** from the [A2A hackathon template](https://github.com/a2anet/a2a-hackathon-template) — required for harness scoring
- **8 pharma safety documents** (`doc_pharma_*.json`) — ADR reporting, missing details, complaints, escalation, verification, tools

The CS agent indexes all documents into Redis on startup (`cs_agent/ingest.py`).

Optional: precompute embeddings for faster startup:

```powershell
cd cs_agent
$env:KB_DOCUMENTS_DIR = "..\kb\documents"
$env:KB_EMBEDDINGS_PATH = "..\kb\embeddings.json"
python precompute_embeddings.py
```

Without embeddings, BM25 search still works; vector search embeds on first query when an API key is available.
