"""Shared Gemini model factory — API key OR Vertex ADC."""
from __future__ import annotations

import os
from contextlib import contextmanager

from langchain_google_genai import ChatGoogleGenerativeAI


@contextmanager
def _without_env_keys(*keys: str):
    """Temporarily remove API key env vars so langchain-google-genai can set them.

    When GOOGLE_API_KEY is already in the environment, the Vertex branch of
    ChatGoogleGenerativeAI skips the express-key path and falls back to ADC.
    """
    saved = {k: os.environ.pop(k) for k in keys if k in os.environ}
    try:
        yield
    finally:
        os.environ.update(saved)


def build_gemini_model() -> ChatGoogleGenerativeAI:
    """Build ChatGoogleGenerativeAI using an API key or Vertex ADC."""
    model = os.getenv("MODEL", "gemini-3.5-flash")
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in (
        "1",
        "true",
    )

    if api_key:
        kwargs: dict = {"model": model, "google_api_key": api_key}
        if use_vertex:
            kwargs["vertexai"] = True
            project = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project:
                kwargs["project"] = project
            kwargs["location"] = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            with _without_env_keys("GOOGLE_API_KEY", "GEMINI_API_KEY"):
                return ChatGoogleGenerativeAI(**kwargs)
        return ChatGoogleGenerativeAI(**kwargs)

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError(
            "No GEMINI_API_KEY / GOOGLE_API_KEY and no GOOGLE_CLOUD_PROJECT. "
            "Either set an API key or configure Vertex ADC "
            "(scripts/setup-adc.ps1)."
        )

    return ChatGoogleGenerativeAI(
        model=model,
        vertexai=True,
        project=project,
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
