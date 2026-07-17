# VbaExtractor

Ein Zwei-Wege-Tool zum Umgang mit VBA-Makros in `.swp`-Dateien (z. B. verschlüsselte/gesperrte Office-Vorlagen).

## Was das Skript macht

`VbaExtractor` unterstützt zwei Konvertierungsrichtungen:

1. **`.swp` → `.txt`**
   Extrahiert den enthaltenen VBA-Code aus einer `.swp`-Datei und speichert alle Module gesammelt in einer lesbaren `.txt`-Datei.

2. **`.txt` → Ordner mit Einzeldateien**
   Rekonstruiert aus einer zuvor erzeugten `.txt`-Datei die einzelnen VBA-Module als separate Dateien (`.bas`, `.cls`, `.frm`, ...) in einem neuen, mit Datum/Uhrzeit benannten Ordner.

Die Dateiendung der Eingabe entscheidet automatisch, welcher Vorgang ausgeführt wird — es kann also dieselbe `.py`-Datei bzw. `.exe` für beide Richtungen verwendet werden.

## Voraussetzungen

- Python 3.8 oder neuer
- Das Python-Paket [`oletools`](https://pypi.org/project/oletools/)

## Installation

1. Python installieren (falls noch nicht vorhanden): [python.org/downloads](https://www.python.org/downloads/)
   Unter Windows beim Installer die Option **"Add Python to PATH"** aktivieren.

2. Benötigtes Paket installieren. Dazu die Eingabeaufforderung (cmd) öffnen und folgenden Befehl ausführen:

   ```bash
   pip install oletools
   ```

3. Repository klonen oder `VbaExtractor.py` herunterladen.

## Nutzung

### Drag & Drop (Windows)

Eine oder mehrere `.swp`- oder `.txt`-Dateien einfach auf `VbaExtractor.py` (oder die daraus gebaute `.exe`) ziehen. Das Skript öffnet eine Konsole, verarbeitet alle übergebenen Dateien nacheinander und wartet am Ende auf Enter.

### Über die Kommandozeile

```bash
python VbaExtractor.py "C:\Pfad\zur\Datei.swp"
python VbaExtractor.py "C:\Pfad\zur\Datei.txt"
```

Es können auch mehrere Dateien gleichzeitig übergeben werden:

```bash
python VbaExtractor.py datei1.swp datei2.swp modul_export.txt
```

## Als eigenständige .exe nutzen (ohne Python-Installation)

Um das Tool ohne separate Python-Installation weiterzugeben, kann es mit [PyInstaller](https://pyinstaller.org/) zu einer eigenständigen `.exe` gebündelt werden. Dies muss einmalig auf einem Windows-Rechner mit installiertem Python ausgeführt werden:

```bash
pip install pyinstaller oletools
pyinstaller --onefile --console --name VbaExtractor VbaExtractor.py
```

Die fertige Datei liegt danach unter `dist\VbaExtractor.exe` und kann auf beliebige andere Windows-Systeme kopiert werden — dort läuft sie ohne weitere Installation.

> **Hinweis:** Falls die `.exe` mit einem `ModuleNotFoundError` abstürzt, hilft meist:
> ```bash
> pyinstaller --onefile --console --name VbaExtractor --hidden-import=olefile --hidden-import=oletools.olevba VbaExtractor.py
> ```

## Beispiel-Ausgabe

Beim Export einer `.swp`-Datei entsteht eine `.txt`-Datei in etwa folgender Form:

```
--- VBA-Export aus: Vorlage.swp ---

 ================================================================================
  >> MODUL: Modul1.bas
 ================================================================================

Sub Beispiel()
    MsgBox "Hallo Welt"
End Sub
```

Beim Rekonstruieren dieser `.txt`-Datei entsteht ein Ordner wie:

```
2026-07-17_14-32_Vorlage/
└── Modul1.bas
```

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
