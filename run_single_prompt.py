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
    input_file = Path("output/cot/cot__ee-security.md")
    output_file = Path("TEST_REQUEST.MD")

    try:
        prompt_text = load_markdown(input_file)
        print(prompt_text)
        response_text = api.query(prompt_text)
        

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(response_text, encoding="utf-8")

        logger.info("Antwort gespeichert unter: %s", output_file.resolve())
        print(f"✅ Antwort gespeichert in {output_file.resolve()}")
    except Exception as e:
        logger.exception("Fehler bei der Verarbeitung: %s", e)
        print("❌ Fehler bei der Verarbeitung – siehe Log.")

    




if __name__ == "__main__":
    main()
