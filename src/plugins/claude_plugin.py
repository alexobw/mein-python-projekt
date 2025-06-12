"""Anthropic Claude API plugin."""

from __future__ import annotations

import logging
import os

import anthropic
from dotenv import load_dotenv

from . import BaseModelPlugin, register_plugin


logger = logging.getLogger(__name__)
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


@register_plugin("claude")
class ClaudePlugin(BaseModelPlugin):
    """Plugin for Anthropic Claude chat completions."""

    def __init__(self) -> None:
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self._client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def query(self, prompt: str) -> str:
        logger.debug("Querying Claude")
        try:
            response = self._client.messages.create(
                model="claude-3.5-sonnet-20240620",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Claude request failed: %s", exc)
            raise RuntimeError(f"Claude request failed: {exc}") from exc
