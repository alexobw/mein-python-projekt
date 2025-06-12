from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_markdown(path: Path) -> str:
    """Load Markdown file from path and return contents."""
    logger.debug("Lese Markdown-Datei: %s", path)
    if not path.exists():
        logger.error("Datei nicht gefunden: %s", path)
        raise FileNotFoundError(f"Datei nicht gefunden: {path}")
    text = path.read_text(encoding="utf-8")
    logger.debug("Datei %s geladen (%d Zeichen)", path, len(text))
    return text
