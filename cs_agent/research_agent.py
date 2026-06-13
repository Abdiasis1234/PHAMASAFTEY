"""Internal Research Agent — medical and regulatory context from the KB."""

import os
import uuid

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from rag_tools import kb_search_bm25, kb_search_vector

MODEL = os.environ.get("MODEL", "gemini-3.5-flash")

RESEARCH_INSTRUCTION = """\
You are a pharmaceutical safety research specialist. Your job is to search the
knowledge base and synthesize findings for the customer service agent.

When given a research question or safety case summary:
1. Search the knowledge base with both kb_search_bm25 (keywords) and
   kb_search_vector (natural-language questions) using multiple query phrasings.
2. Extract relevant procedures, eligibility rules, escalation paths, tool names,
   regulatory requirements, and safety thresholds.
3. Return a concise research brief with:
   - key findings (bullet points)
   - recommended procedures or next steps from the KB
   - any gaps where the KB has no coverage
   - urgency or escalation flags if the case warrants it

Do not invent policies. If the KB has no answer after rephrasing searches,
say so clearly.
"""

research_agent = LlmAgent(
    name="research_agent",
    model=MODEL,
    instruction=RESEARCH_INSTRUCTION,
    tools=[kb_search_bm25, kb_search_vector],
)

_session_service = InMemorySessionService()
_runner = Runner(
    agent=research_agent,
    app_name="pharma_research",
    session_service=_session_service,
)


async def run_research(query: str, session_key: str) -> str:
    """Run the internal research agent and return its synthesis."""
    session = await _session_service.create_session(
        app_name="pharma_research",
        user_id="cs_agent",
        session_id=f"{session_key}-research-{uuid.uuid4().hex[:8]}",
    )
    user_content = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )
    final_text = ""
    async for event in _runner.run_async(
        user_id="cs_agent",
        session_id=session.id,
        new_message=user_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text = part.text
    return final_text or "[research agent returned no findings]"
