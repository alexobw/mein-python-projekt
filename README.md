# Mein Python Projekt

Dieses Repository erzeugt Prompts für verschiedene Migrationsaufgaben und lässt sie von Sprachmodellen beantworten.

## Ablauf

1. **Prompts erstellen**
   ```bash
   python prompt_builder.py
   ```
   Das Skript erzeugt alle Kombinationen aus Strategie und Aufgabe und legt sie unter `output/<strategie>/<strategie>__<aufgabe>.md` ab.

2. **Prompts ausführen**
   ```bash
   python prompt_runner.py --api <openai|claude|gemini>
   ```
   `src/prompt_runner.py` liest alle Dateien im `output`-Ordner ein, schickt sie über die gewählte API ab und speichert die Antworten unter `responses/<api>/<prompt>-response.md`.

## Benötigte Umgebungsvariablen

Die API-Schlüssel werden aus einer `.env`-Datei geladen. Je nach verwendeter API müssen folgende Variablen gesetzt sein:

- `OPENAI_API_KEY` für OpenAI
- `ANTHROPIC_API_KEY` für Claude
- `GEMINI_API_KEY` für Google Gemini

## Ordnerstruktur

```
output/
  <strategie>/
    <strategie>__<aufgabe>.md
responses/
  <api>/
    <prompt>-response.md
```

Damit arbeiten `prompt_builder.py` und `prompt_runner.py` zusammen: Erst erzeugt `prompt_builder.py` die Prompt-Dateien im `output`-Verzeichnis, anschließend holt sich `prompt_runner.py` diese Dateien und legt die Modellantworten im `responses`-Verzeichnis ab.
