from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.loader import load_markdown


def test_load_markdown(tmp_path: Path) -> None:
    file = tmp_path / "sample.md"
    file.write_text("hello", encoding="utf-8")
    assert load_markdown(file) == "hello"
