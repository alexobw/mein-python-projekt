from pathlib import Path
import logging

from src.logging_config import setup_logging
from src.loader import load_markdown
from src.prompt_builder import PromptBuilder
from src.config.strategy_map import STRATEGY_MAP
from src.config.task_map import TASK_MAP


def main() -> None:
    """Erzeuge alle Prompt-Kombinationen."""
    setup_logging("logs/prompt_builder.log")
    logger = logging.getLogger(__name__)
    logger.info("Starte Prompt Builder")

    project_root = Path(__file__).resolve().parent

    structure_path = project_root / "data" / "strukturen" / "grundstruktur.md"
    structure_text = load_markdown(structure_path)

    builder = PromptBuilder(structure_text)

    for strategy, strategy_path in STRATEGY_MAP.items():
        strategy_text = load_markdown(project_root / strategy_path)
        for task, task_path in TASK_MAP.items():
            task_text = load_markdown(project_root / task_path)
            prompt = builder.build_prompt(task_text, strategy_text)

            out_dir = project_root / "output" / strategy
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{strategy}__{task}.md"
            out_path.write_text(prompt, encoding="utf-8")
            logger.info("Prompt gespeichert unter: %s", out_path.resolve())

    logger.info("Prompt Builder beendet")


if __name__ == "__main__":
    main()
