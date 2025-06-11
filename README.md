# Mein Python Projekt

Dieses Projekt erstellt automatisch Prompts basierend auf verschiedenen Aufgaben und Strategien.

## Vorbereitung
Alle benötigten Eingabedateien befinden sich im Ordner `data`.

## Ausführen
```
python run.py --strategy <strategie> --task <aufgabe>
```
Verfügbare Strategien sind in `src/config/strategy_map.py` aufgeführt, mögliche Aufgaben in `src/config/task_map.py`.

Die generierten Prompts werden im Ordner `output/<strategie>` gespeichert.
