import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.plugins import factory
import pytest

pytest.importorskip("openai")
import src.plugins.openai_plugin  # noqa: F401


def test_factory_creates_plugin() -> None:
    plugin = factory.create("openai")
    assert plugin is not None
