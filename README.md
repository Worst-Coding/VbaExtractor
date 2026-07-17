# VbaExtractor

.swp to .txt - VbaExtractor ist ein Zwei-Wege-Tool zum Umgang mit VBA-Makros in .swp-Dateien.

English: .swp to .txt - VbaExtractor is a two-way tool for working with VBA macros in .swp files.

## Features

- Extrahiert VBA-Makros aus .swp-Dateien und speichert sie als lesbare `.txt`-Dateien.
- Ermöglicht die Rückschreibung (Two-way): Änderungen in `.txt` können wieder in `.swp` integriert werden.
- Nützlich für Analyse, Code-Review und Forensik von VBA-Makros.

## Installation

1. Repository klonen:

```bash
git clone https://github.com/Worst-Coding/VbaExtractor.git
cd VbaExtractor
```

2. (Optional) Eine passende Laufzeit installieren (z. B. Python, Node.js). Siehe Projektdateien für Details.

## Benutzung

- Extrahieren:

```bash
# Beispielkommando — bitte an die tatsächliche Implementierung anpassen
vbaextractor extract input_file.swp -o output_dir/
```

- Rückschreiben (Inject):

```bash
# Beispielkommando — bitte an die tatsächliche Implementierung anpassen
vbaextractor inject modified_macro.txt -i original_file.swp -o updated_file.swp
```

Hinweis: Die genauen CLI-Optionen hängen von der Implementierung ab. Ergänze oder passe diese Beispiele an, wenn die Befehle im Projekt festgelegt sind.

## Beispiele / Use cases

- Makroanalyse: Makros extrahieren, durchlesen und auf verdächtiges Verhalten prüfen.
- Batch-Verarbeitung: Mehrere `.swp`-Dateien in einem Skript verarbeiten.
- Forensik / Incident Response: Makrocodes aus beschädigten Dateien rekonstruieren.

## Contribution

Beiträge, Issues und Verbesserungsvorschläge sind willkommen. Öffne ein Issue oder erstelle einen Pull Request.

## Lizenz

Bitte eine Lizenzdatei (`LICENSE`) zum Repository hinzufügen oder diesen Abschnitt entsprechend anpassen.

## Kontakt

Für Fragen oder Hilfestellung: Öffne ein Issue im Repository.
