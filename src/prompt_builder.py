import logging

logger = logging.getLogger(__name__)


class PromptBuilder:
    def __init__(self, template: str):
        logger.debug("Initialisiere PromptBuilder")
        self.template = template

    def build_prompt(self, task_text: str, strategy_text: str) -> str:
        logger.debug("Baue Prompt")
        prompt = (
            self.template.replace("[Promptstrategie]", strategy_text.strip())
            .replace("[Migrationsaufgabe]", task_text.strip())
        )
        logger.debug("Prompt erstellt (%d Zeichen)", len(prompt))
        return prompt
