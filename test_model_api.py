from src.model_api import ModelAPI

if __name__ == "__main__":
    prompt = "Erkläre mir den Unterschied zwischen Zero-Shot und One-Shot Prompting."

    api = ModelAPI()

    print("🔷 OpenAI GPT-4o:\n", api.query_openai(prompt))
    # print("\n🟡 Claude 3.5:\n", api.query_claude(prompt))
    # print("\n🔴 Gemini:\n", api.query_gemini(prompt))