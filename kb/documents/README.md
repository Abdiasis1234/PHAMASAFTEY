# Knowledge base documents

698 JSON documents for the Rho-Bank A2A hackathon harness. Indexed into Redis by `cs_agent/ingest.py` at startup.

Optional: precompute embeddings for faster startup (requires `GOOGLE_API_KEY`):

```powershell
cd cs_agent
$env:KB_DOCUMENTS_DIR = "..\kb\documents"
$env:KB_EMBEDDINGS_PATH = "..\kb\embeddings.json"
python precompute_embeddings.py
```

Source: [a2anet/a2a-hackathon-template](https://github.com/a2anet/a2a-hackathon-template/tree/main/kb/documents)
