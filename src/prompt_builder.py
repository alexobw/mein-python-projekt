class PromptBuilder:
    def __init__(self, template: str):
        self.template = template

    def build_prompt(self, task_text: str, strategy_text: str) -> str:
        return self.template.replace("[Promptstrategie]", strategy_text.strip()) \
                            .replace("[Migrationsaufgabe]", task_text.strip())
