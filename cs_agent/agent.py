"""Pharma safety customer service agent: policy + env tools + KB + research."""

import os
from pathlib import Path

from google.adk.agents import LlmAgent

from env_toolset import EnvApiToolset
from rag_tools import kb_search_bm25, kb_search_vector
from research_tool import ask_research_agent

MODEL = os.environ.get("MODEL", "gemini-3.5-flash")
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_POLICY = _REPO_ROOT / "kb" / "policy.md"
POLICY_PATH = Path(os.environ.get("KB_POLICY_PATH", _DEFAULT_POLICY if _DEFAULT_POLICY.exists() else "/app/kb/policy.md"))

RAG_GUIDANCE = """

## Knowledge Base and Research Agent

You do NOT have the knowledge base inlined. For policy questions or
scenario-specific procedures:

1. **ask_research_agent(query)** — preferred for complex cases. The internal
   Research Agent runs multiple KB searches and returns a synthesized brief
   with procedures, escalation paths, and regulatory context. Use this when you
   receive a structured safety case or need to decide the correct next action.

2. **Direct search** — for quick lookups you can also call:
   - kb_search_bm25(query): keyword search
   - kb_search_vector(query): semantic search for natural-language questions

Search before you act. Procedures, eligibility rules, internal tool names,
and scenario-specific guidance all live in the knowledge base. If a search
comes up empty, rephrase and try again (or ask the Research Agent) before
telling the customer you cannot find the information.

## Structured safety cases

The personal agent may send structured JSON with fields like case_type,
medicine, symptoms, severity, missing_fields, urgency, and summary. Use these
to prioritize urgency, identify missing information to request, and choose the
correct procedure from the knowledge base.
"""

root_agent = LlmAgent(
    name="cs_agent",
    model=MODEL,
    instruction=POLICY_PATH.read_text() + RAG_GUIDANCE,
    tools=[
        EnvApiToolset(),
        ask_research_agent,
        kb_search_bm25,
        kb_search_vector,
    ],
)
