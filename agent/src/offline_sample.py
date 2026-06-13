"""Canned dashboard inputs for OFFLINE=1 mode.

When OFFLINE=1 is set, the /fixed agent serves a deterministic sample
safety-case dashboard with NO Gemini call and no API key.
"""
from __future__ import annotations

from typing import Any

OFFLINE_DASHBOARD_ARGS: dict[str, Any] = {
    "eyebrow": "SAFETY CASE · ADR INTAKE",
    "title": "ExampleMed — Moderate ADR",
    "subtitle": "Patient reports dizziness and nausea after starting ExampleMed 10mg. Missing dosage timing.",
    "kpis": [
        {
            "label": "Case type",
            "value": "ADR",
            "delta": "",
            "caption": "Adverse drug reaction",
        },
        {
            "label": "Severity",
            "value": "Moderate",
            "delta": "",
            "caption": "Limits daily activity; no hospitalization",
        },
        {
            "label": "Urgency",
            "value": "High",
            "delta": "",
            "caption": "PV follow-up within 24h if serious criteria met",
        },
        {
            "label": "Missing fields",
            "value": "2",
            "delta": "",
            "caption": "dosage timing, patient age band",
        },
    ],
    "trend": [
        {"label": "Day 0", "value": 0.0},
        {"label": "Day 1", "value": 1.0},
        {"label": "Day 2", "value": 2.0},
        {"label": "Day 3", "value": 4.0},
        {"label": "Day 4", "value": 5.0},
        {"label": "Day 5", "value": 6.0},
    ],
    "share": [
        {"label": "Dizziness", "value": 45.0},
        {"label": "Nausea", "value": 35.0},
        {"label": "Fatigue", "value": 20.0},
    ],
    "rows": [
        {
            "name": "Medicine",
            "category": "Product",
            "value": "ExampleMed 10mg",
            "delta": "",
        },
        {
            "name": "Reporter",
            "category": "Source",
            "value": "Patient",
            "delta": "",
        },
        {
            "name": "Onset",
            "category": "Timeline",
            "value": "48h after start",
            "delta": "",
        },
        {
            "name": "Next action",
            "category": "Workflow",
            "value": "Request missing fields",
            "delta": "",
        },
        {
            "name": "Escalation",
            "category": "Regulatory",
            "value": "PV review if worsens",
            "delta": "",
        },
    ],
    "scope_options": [
        {"label": "Intake summary", "value": "intake"},
        {"label": "Symptoms", "value": "symptoms"},
        {"label": "Missing info", "value": "missing"},
        {"label": "Escalation path", "value": "escalation"},
    ],
    "scope_selected": "intake",
}
