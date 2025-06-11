# Mein Python Projekt

Dieses Repository erzeugt Prompts für verschiedene Migrationsaufgaben und lässt sie von Sprachmodellen beantworten.

## Ablauf

1. **Prompt erstellen**
   ```bash
   python run.py --strategy <strategie> --task <aufgabe> --data local
   ```
   Das Skript ruft `src.main.main` auf und schreibt den fertigen Prompt nach `output/<strategie>/<strategie>__<aufgabe>.md`.

2. **Prompt ausführen**
   ```bash
   python -m src.prompt_runner --api <openai|claude|gemini>
   ```
   `src/prompt_runner.py` liest alle Dateien im `output`-Ordner ein, schickt sie über die gewählte API ab und speichert die Antworten unter `responses/<api>/<strategie>/<strategie>__<aufgabe>.md`.

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
    <strategie>/
      <strategie>__<aufgabe>.md
```

Damit arbeiten `run.py` und `src/prompt_runner.py` zusammen: Erst erzeugt `run.py` die Prompt-Dateien im `output`-Verzeichnis, anschließend holt sich `prompt_runner.py` diese Dateien und legt die Modellantworten im `responses`-Verzeichnis ab.
