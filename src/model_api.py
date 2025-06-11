import os
from dotenv import load_dotenv

# API-Clients
from openai import OpenAI
import anthropic
import google.generativeai as genai

# .env einlesen
load_dotenv()

# API-Keys auslesen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ModelAPI:
    def __init__(self):
        # Initialisiere Clients nur bei Bedarf
        self._openai_client = None
        self._anthropic_client = None
        self._gemini_model = None

    def query_openai(self, prompt: str) -> str:
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY fehlt in .env")

        if not self._openai_client:
            self._openai_client = OpenAI(api_key=OPENAI_API_KEY)

        try:
            response = self._openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            raise RuntimeError(f"OpenAI Anfrage fehlgeschlagen: {exc}") from exc

    def query_claude(self, prompt: str) -> str:
        if not ANTHROPIC_API_KEY:
            raise ValueError("❌ ANTHROPIC_API_KEY fehlt in .env")

        if not self._anthropic_client:
            self._anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        try:
            response = self._anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            raise RuntimeError(f"Claude Anfrage fehlgeschlagen: {exc}") from exc

    def query_gemini(self, prompt: str) -> str:
        if not GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY fehlt in .env")

        if not self._gemini_model:
            genai.configure(api_key=GEMINI_API_KEY)
            self._gemini_model = genai.GenerativeModel("gemini-1.5-pro-latest")

        chat = self._gemini_model.start_chat()
        try:
            response = chat.send_message(
                prompt, generation_config={"temperature": 0}
            )
            return response.text.strip()
        except Exception as exc:
            raise RuntimeError(f"Gemini Anfrage fehlgeschlagen: {exc}") from exc
