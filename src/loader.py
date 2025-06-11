from pathlib import Path

def load_markdown(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")
    return path.read_text(encoding="utf-8")
