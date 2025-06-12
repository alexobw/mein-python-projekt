"""Model API plugin system."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Type


logger = logging.getLogger(__name__)


class BaseModelPlugin(ABC):
    """Abstract base class for model API plugins."""

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Send a prompt to the API and return the response."""


@dataclass
class PluginFactory:
    """Factory that manages available plugins."""

    registry: Dict[str, Type[BaseModelPlugin]]

    def register(self, name: str, plugin: Type[BaseModelPlugin]) -> None:
        logger.debug("Registering plugin %s", name)
        self.registry[name] = plugin

    def create(self, name: str) -> BaseModelPlugin:
        if name not in self.registry:
            raise ValueError(f"Unknown plugin: {name}")
        logger.debug("Creating plugin instance for %s", name)
        return self.registry[name]()


factory = PluginFactory(registry={})


def register_plugin(name: str) -> callable:
    """Decorator to register plugin classes."""

    def wrapper(cls: Type[BaseModelPlugin]) -> Type[BaseModelPlugin]:
        factory.register(name, cls)
        return cls

    return wrapper


# Try to import default plugins so they register themselves.  Missing optional
# dependencies are ignored so the package can be used without every API
# library installed.
for _plugin in ("openai_plugin", "claude_plugin", "gemini_plugin"):
    try:  # pragma: no cover - optional imports
        __import__(f"src.plugins.{_plugin}")
    except Exception as exc:  # noqa: BLE001
        logger.debug("Plugin %s not loaded: %s", _plugin, exc)
