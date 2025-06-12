"""Google Gemini API plugin."""

from __future__ import annotations

import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

from . import BaseModelPlugin, register_plugin


logger = logging.getLogger(__name__)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@register_plugin("gemini")
class GeminiPlugin(BaseModelPlugin):
    """Plugin for Google Gemini chat completions."""

    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=GEMINI_API_KEY)
        self._model = genai.GenerativeModel("gemini-1.5-pro-latest")

    def query(self, prompt: str) -> str:
        logger.debug("Querying Gemini")
        try:
            response = self._model.generate_content(prompt)
            return response.text.strip()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Gemini request failed: %s", exc)
            raise RuntimeError(f"Gemini request failed: {exc}") from exc
