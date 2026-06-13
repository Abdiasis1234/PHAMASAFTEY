"""Fixed-schema dashboard agent for pharmaceutical safety intake.

The user describes an unstructured safety concern in chat. The agent extracts
structured case fields and calls `render_dashboard` to paint a safety-case
dashboard on the A2UI canvas.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import TypedDict

from copilotkit import CopilotKitMiddleware, a2ui
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

from src.catalog import CATALOG_ID, CATALOG_PROMPT

SCHEMA_DIR = Path(__file__).parent / "a2ui" / "schemas"
DASHBOARD_SCHEMA = a2ui.load_schema(SCHEMA_DIR / "dashboard.json")
SURFACE = "safety-dashboard"


# NOTE (Gemini typed-array fix): every list parameter on render_dashboard
# below is typed as `list[<TypedDict>]`, NOT `list[dict]`. Gemini's
# function-declaration validator rejects untyped arrays with
# "parameters.properties[X].items: missing field". A TypedDict compiles to a
# concrete object schema, so these arrays carry the `items` Gemini requires.
# Keep them typed — do not loosen to `list[dict]`.
class Kpi(TypedDict):
    label: str
    value: str
    delta: str
    caption: str


class Point(TypedDict):
    label: str
    value: float


class Row(TypedDict):
    name: str
    category: str
    value: str
    delta: str


class ScopeOption(TypedDict):
    label: str
    value: str


@tool
def render_dashboard(
    eyebrow: str,
    title: str,
    subtitle: str,
    kpis: list[Kpi],
    trend: list[Point],
    share: list[Point],
    rows: list[Row],
    scope_options: list[ScopeOption],
    scope_selected: str,
) -> str:
    """Render the pharmaceutical safety case dashboard.

    Pass extracted case data INLINE. Call ONCE per turn.

    Map safety fields into the dashboard schema:
      - kpis: EXACTLY 4 cards — e.g. case type, severity, urgency, missing field count.
        Use value for the headline, delta for change indicators (often ""), caption for context.
      - trend: 6–12 points — symptom intensity or timeline (label = day/time, value = score).
      - share: 3–5 slices — symptom mix or concern categories (percentages as numbers).
      - rows: 5–8 rows — key extracted fields (medicine, reporter, onset, next action, etc.).
      - scope_options: 3–6 chips — intake summary, symptoms, missing info, escalation path.
      - scope_selected: active chip value.
    """
    payload = {
        "eyebrow": eyebrow,
        "title": title,
        "subtitle": subtitle,
        "kpis": kpis,
        "trend": trend,
        "share": share,
        "rows": rows,
        "scope": {"options": scope_options, "selected": scope_selected},
    }
    return a2ui.render(
        operations=[
            a2ui.create_surface(SURFACE, catalog_id=CATALOG_ID),
            a2ui.update_components(SURFACE, DASHBOARD_SCHEMA),
            a2ui.update_data_model(SURFACE, payload),
        ]
    )


SYSTEM_PROMPT = f"""\
You are a pharmaceutical safety intake assistant for PhamaSafety.

## Your job

When a user describes a medicine safety concern (adverse reaction, missing
patient details, quality complaint, or escalation request), you:

1. Extract structured fields: case_type, medicine, symptoms, severity
   (mild/moderate/severe/critical), urgency (low/medium/high/critical),
   missing_fields, reporter type, and a one-line summary.
2. Call `render_dashboard(...)` ONCE to paint the safety-case dashboard.
3. Briefly explain what you found and what information is still needed.

Behind the scenes, a Personal Agent (:9001) and Customer Service Agent (:9002)
handle policy, verification, and KB research over A2A — you focus on intake
and the structured dashboard view.

## When to render

Render the dashboard when:
  - The user first describes a safety concern
  - They ask to "show the case" or "render the dashboard"
  - They click a scope chip (delivered as log_a2ui_event with select_chip)
  - They provide new details that change severity, urgency, or missing fields

## Dashboard mapping

  - KPIs: case type, severity, urgency, count of missing fields
  - Trend: symptom timeline or intensity over days
  - Share: symptom or concern category breakdown
  - Rows: medicine, reporter, onset, recommended next action, escalation status
  - Scope chips: Intake summary, Symptoms, Missing info, Escalation path

## Hard rules

- Call `render_dashboard` AT MOST ONCE per turn.
- Be empathetic — reporters may be distressed.
- Never invent medical outcomes or regulatory decisions.
- If the user asks for ad-hoc charts beyond this layout, suggest the Dynamic tab.
- For simple questions ("what does moderate severity mean?"), answer in chat without re-rendering.

{CATALOG_PROMPT}
"""


# Gemini 3.5 Flash via the native Google Gen AI SDK — same provider as the
# dynamic agent and the PDF extractor (see FROZEN.md "LLM provider"). The
# native SDK replays Gemini's thought_signature across tool turns, which the
# OpenAI-compat path does not.
#
# Constructed lazily (not at import time): ChatGoogleGenerativeAI validates
# the API key in its constructor and raises with no key. Building it lazily
# lets `import main` succeed with OFFLINE=1 and no key (the offline branch of
# build_fixed_agent never touches the live model). Online behavior is
# unchanged — the client is built on the first build_fixed_agent() call.
def _build_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=os.getenv("MODEL", "gemini-3.5-flash"),
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def build_fixed_agent():
    if os.getenv("OFFLINE") == "1":
        # CUSTOMIZATION SEAM (offline): no Gemini call, no API key. A
        # deterministic stub chat model drives the REAL create_agent ReAct
        # loop + the REAL render_dashboard tool, so the emitted A2UI envelope
        # is byte-for-byte the production shape (createSurface +
        # updateComponents + updateDataModel wrapped in a2ui_operations).
        from src.offline_fixed import build_offline_fixed_agent

        return build_offline_fixed_agent(render_dashboard, SYSTEM_PROMPT)

    return create_agent(
        model=_build_model(),
        tools=[render_dashboard],
        # CopilotKitMiddleware forwards frontend tools + agent context (e.g.
        # useAgentContext payloads) to the LLM.
        middleware=[CopilotKitMiddleware()],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )


graph = build_fixed_agent()
