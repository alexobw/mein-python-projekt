# Mein Python Projekt

Dieses Repository erzeugt Prompts für verschiedene Migrationsaufgaben und lässt sie von Sprachmodellen beantworten.

## Ablauf

1. **Prompts erstellen**
   ```bash
   python prompt_builder.py
   ```
Das Skript erzeugt alle Kombinationen aus Strategie und Aufgabe und legt sie unter `output/<strategie>/<strategie>__<aufgabe>.md` ab.
Alle Aktivitäten werden in `logs/prompt_builder.log` protokolliert.

2. **Prompts ausführen**
   ```bash
   python prompt_runner.py --api <openai|claude|gemini>
   ```
`prompt_runner.py` liest alle Dateien im `output`-Ordner ein, schickt sie über die gewählte API ab und speichert die Antworten unter `responses/<api>/<prompt>-response.md`. Ein detailliertes Log findet sich in `logs/prompt_runner.log`.
Die Anbindung an die verschiedenen APIs erfolgt über ein flexibles Plugin-System. Beim Import des Pakets `src.plugins` werden die vorhandenen Plugins automatisch geladen, sofern ihre Abhängigkeiten installiert sind. Eigene Plugins können unter `src/plugins` hinzugefügt werden.

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
logs/
  prompt_builder.log
  prompt_runner.log
```

Damit arbeiten `prompt_builder.py` und `prompt_runner.py` zusammen: Erst erzeugt `prompt_builder.py` die Prompt-Dateien im `output`-Verzeichnis, anschließend holt sich `prompt_runner.py` diese Dateien und legt die Modellantworten im `responses`-Verzeichnis ab.
Die Hilfsfunktionen liegen im Ordner `src`, während die beiden ausführbaren Skripte direkt im Projektstamm zu finden sind.
Neue Modelle können über das Plugin-System einfach ergänzt werden.
\nZum Ausführen der Unit-Tests:\n\n


Zum Ausführen der Unit-Tests:

```bash
pytest
```
