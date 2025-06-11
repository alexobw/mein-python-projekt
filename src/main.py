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
    parser.add_argument("--data", required=True, choices=["local", "remote"])

    args = parser.parse_args()

    structure_path = Path("data/strukturen/grundstruktur.md")
    structure_text = load_markdown(structure_path)
    strategy_text = load_markdown(STRATEGY_MAP[args.strategy])
    task_text = load_markdown(TASK_MAP[args.task])

    builder = PromptBuilder(structure_text)
    prompt = builder.build_prompt(task_text, strategy_text)

    # Ausgabeordnerstruktur: output/<strategy>/
    base_output = Path("output") / args.strategy
    base_output.mkdir(parents=True, exist_ok=True)

    output_file = base_output / f"{args.strategy}__{args.task}.md"
    output_file.write_text(prompt, encoding="utf-8")

    print(f"✅ Prompt gespeichert unter: {output_file.resolve()}")



    

if __name__ == "__main__":
    main()