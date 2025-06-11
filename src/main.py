# main.py
import argparse
from pathlib import Path
from src.loader import load_markdown
from src.prompt_builder import PromptBuilder
from src.config.strategy_map import STRATEGY_MAP
from src.config.task_map import TASK_MAP

def main() -> None:
    parser = argparse.ArgumentParser(description="Baue LLM-Prompt aus Aufgabe und Strategie.")
    parser.add_argument("--strategy", required=True, choices=list(STRATEGY_MAP.keys()))
    parser.add_argument("--task", required=True, choices=list(TASK_MAP.keys()))

    args = parser.parse_args()

    # Ermittle Projektwurzel relativ zu dieser Datei, damit das Skript
    # auch von anderen Arbeitsverzeichnissen aufgerufen werden kann.
    project_root = Path(__file__).resolve().parent.parent

    structure_path = project_root / "data" / "strukturen" / "grundstruktur.md"
    structure_text = load_markdown(structure_path)
    strategy_text = load_markdown(project_root / STRATEGY_MAP[args.strategy])
    task_text = load_markdown(project_root / TASK_MAP[args.task])

    builder = PromptBuilder(structure_text)
    prompt = builder.build_prompt(task_text, strategy_text)

    # Ausgabeordnerstruktur: output/<strategy>/
    base_output = project_root / "output" / args.strategy
    base_output.mkdir(parents=True, exist_ok=True)

    output_file = base_output / f"{args.strategy}__{args.task}.md"
    output_file.write_text(prompt, encoding="utf-8")

    print(f"✅ Prompt gespeichert unter: {output_file.resolve()}")



    

if __name__ == "__main__":
    main()
