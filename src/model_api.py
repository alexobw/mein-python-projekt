"""High-level interface for querying model APIs via plugins."""

from __future__ import annotations

import logging
from typing import Iterable

from src.plugins import BaseModelPlugin, factory  # type: ignore  # local import


logger = logging.getLogger(__name__)


class ModelAPI:
    """Facade to run prompts through registered model plugins."""

    def __init__(self, plugin_name: str) -> None:
        logger.debug("Initialising ModelAPI with plugin %s", plugin_name)
        self._plugin: BaseModelPlugin = factory.create(plugin_name)

    def query(self, prompt: str) -> str:
        """Return the completion for a single prompt."""
        logger.debug("Querying plugin %s", type(self._plugin).__name__)
        return self._plugin.query(prompt)

    def query_all(self, prompts: Iterable[str]) -> list[str]:
        """Return completions for all prompts."""
        results: list[str] = []
        for prompt in prompts:
            results.append(self.query(prompt))
        return results
