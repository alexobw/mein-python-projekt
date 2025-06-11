import argparse
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

    api = ModelAPI()
    query_fn = getattr(api, f"query_{args.api}")

    for prompt_file in gather_prompt_files(Path("output")):
        prompt_text = load_markdown(prompt_file)
        strategy = prompt_file.parent.name
        task = prompt_file.stem.split("__", 1)[1]

        response_text = query_fn(prompt_text)

        out_dir = Path("responses") / args.api / strategy
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{strategy}__{task}.md"
        out_path.write_text(response_text, encoding="utf-8")
        print(f"✅ Antwort gespeichert unter: {out_path.resolve()}")


if __name__ == "__main__":
    main()
