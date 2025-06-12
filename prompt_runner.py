"""Run all prompts through a selected API."""

import argparse
import logging
from pathlib import Path

from uuid import uuid4

from src.logging_config import setup_logging
from src.loader import load_markdown
from src.model_api import ModelAPI


def gather_prompt_files(base_dir: Path, logger: logging.LoggerAdapter) -> list[Path]:
    """Collect prompt Markdown files below base_dir."""
    files = sorted(base_dir.glob("*/*.md"))
    logger.debug("%d Prompt-Dateien gefunden", len(files))
    return files


def main() -> None:
    """Send all prompts to selected API and store responses."""
    parser = argparse.ArgumentParser(
        description=(
            "Führt alle gespeicherten Prompts über eine API aus und speichert die Antworten."
        )
    )
    parser.add_argument(
        "--api",
        required=True,
        choices=["openai", "claude", "gemini"],
        help="Zu verwendende API",
    )
    args = parser.parse_args()

    setup_logging("logs/prompt_runner.log")
    correlation_id = uuid4().hex
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra={"corr_id": correlation_id})
    logger.info("Starte Prompt Runner mit API %s", args.api)

    api = ModelAPI(args.api)

    for prompt_file in gather_prompt_files(Path("output"), logger):
        logger.info("Sende Prompt %s an %s", prompt_file.name, args.api)
        try:
            prompt_text = load_markdown(prompt_file)
            response_text = api.query(prompt_text)

            out_dir = Path("responses") / args.api
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{prompt_file.stem}-response.md"
            out_path.write_text(response_text, encoding="utf-8")
            logger.info("Antwort gespeichert unter: %s", out_path.resolve())
        except Exception as exc:
            logger.exception("Fehler bei Verarbeitung von %s: %s", prompt_file, exc)

    logger.info("Prompt Runner beendet")


if __name__ == "__main__":
    main()
