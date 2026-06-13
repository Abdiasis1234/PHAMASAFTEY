"""Tool that lets the CS agent invoke the internal Research Agent."""

from google.adk.tools import ToolContext

from env_toolset import session_id
from research_agent import run_research


async def ask_research_agent(research_query: str, tool_context: ToolContext) -> str:
    """Consult the internal Research Agent for medical and regulatory context.

    Use this before answering complex policy questions, deciding escalation paths,
    or when you need synthesized findings from the knowledge base. Provide a
    clear question or paste the structured safety case fields you received.

    Args:
        research_query: What to research — e.g. escalation criteria for adverse
            drug reactions, required fields for safety reports, or procedure
            for a specific case type.
    """
    return await run_research(research_query, session_id(tool_context))
