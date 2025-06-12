import argparse
import logging
from pathlib import Path

from src.loader import load_markdown
from src.model_api import ModelAPI


def gather_prompt_files(base_dir: Path) -> list[Path]:
    return sorted(base_dir.glob("*/*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Führt alle gespeicherten Prompts über eine API aus und speichert die Antworten.")
    parser.add_argument(
        "--api",
        required=True,
        choices=["openai", "claude", "gemini"],
        help="Zu verwendende API",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    api = ModelAPI()
    query_fn = getattr(api, f"query_{args.api}")

    for prompt_file in gather_prompt_files(Path("output")):
        logging.info("Sende Prompt %s an %s", prompt_file.name, args.api)
        try:
            prompt_text = load_markdown(prompt_file)
            response_text = query_fn(prompt_text)

            out_dir = Path("responses") / args.api
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{prompt_file.stem}-response.md"
            out_path.write_text(response_text, encoding="utf-8")
            logging.info("Antwort gespeichert unter: %s", out_path.resolve())
        except Exception as exc:
            logging.exception("Fehler bei Verarbeitung von %s: %s", prompt_file, exc)


if __name__ == "__main__":
    main()
