from src.model_api import ModelAPI
from dotenv import load_dotenv
import logging

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)

PROMPT = "Welche Farbe hat der Himmel"


def query_openai():
    print("\n🔹 Anfrage an: OPENAI")
    try:
        api = ModelAPI("openai")
        response = api.query(PROMPT)
        print(f"Antwort von OpenAI: {response}")
    except Exception as e:
        print(f"❌ Fehler bei OpenAI: {e}")


def query_claude():
    print("\n🔹 Anfrage an: CLAUDE")
    try:
        api = ModelAPI("claude")
        response = api.query(PROMPT)
        print(f"Antwort von Claude: {response}")
    except Exception as e:
        print(f"❌ Fehler bei Claude: {e}")


def query_gemini():
    print("\n🔹 Anfrage an: GEMINI")
    try:
        api = ModelAPI("gemini")
        response = api.query(PROMPT)
        print(f"Antwort von Gemini: {response}")
    except Exception as e:
        print(f"❌ Fehler bei Gemini: {e}")


if __name__ == "__main__":
    # Du kannst hier beliebig die Funktionen einzeln aufrufen
    #query_openai()
    query_claude()
    #query_gemini()