"""OpenAI API plugin."""

from __future__ import annotations

import logging
import os

import openai
from dotenv import load_dotenv

from . import BaseModelPlugin, register_plugin


logger = logging.getLogger(__name__)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@register_plugin("openai")
class OpenAIPlugin(BaseModelPlugin):
    """Plugin for OpenAI chat completions."""

    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set")
        self._client = openai.Client(api_key=OPENAI_API_KEY)

    def query(self, prompt: str) -> str:
        logger.debug("Querying OpenAI")
        try:
            response = self._client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:  # noqa: BLE001
            logger.exception("OpenAI request failed: %s", exc)
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc
