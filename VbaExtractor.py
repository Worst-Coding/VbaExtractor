"""
================================================================================
 VbaExtractor
================================================================================

WAS DIESES SKRIPT MACHT
--------------------------------------------------------------------------------
VbaExtractor ist ein Zwei-Wege-Tool zum Umgang mit VBA-Makros in .swp-Dateien:

  1) .swp  ->  .txt
     Extrahiert den enthaltenen VBA-Code aus einer .swp-Datei und speichert
     alle Module gesammelt in einer lesbaren .txt-Datei.

  2) .txt  ->  Ordner mit Einzeldateien
     Nimmt eine zuvor erzeugte .txt-Datei und rekonstruiert daraus die
     einzelnen VBA-Module als separate Dateien (.bas, .cls, .frm, ...) in
     einem neuen, mit Datum/Uhrzeit benannten Ordner.

BEDIENUNG (Drag & Drop)
--------------------------------------------------------------------------------
Einfach eine oder mehrere .swp- oder .txt-Dateien per Drag & Drop auf das
Skript ziehen. Das Skript erkennt anhand der Dateiendung automatisch, welcher
Vorgang ausgeführt werden soll.

VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.8 oder neuer
- Das Python-Paket "oletools"

INSTALLATION
--------------------------------------------------------------------------------
1) Python installieren (falls noch nicht vorhanden):
   https://www.python.org/downloads/
   WICHTIG: Beim Installer unter Windows die Option
   "Add Python to PATH" aktivieren.

2) Benötigtes Paket installieren. Dazu die Eingabeaufforderung (cmd) öffnen
   und folgenden Befehl ausführen:
   
        python
        pip install oletools

3) Skript ausführen, z.B. per Drag & Drop einer .swp- oder .txt-Datei auf
   VbaExtractor.py, oder über die Konsole:

       python VbaExtractor.py "C:\Pfad\zur\Datei.swp"

ALS EIGENSTÄNDIGE .EXE NUTZEN (ohne Python-Installation)
--------------------------------------------------------------------------------
Wer das Skript ohne separate Python-Installation weitergeben möchte, kann es
mit PyInstaller zu einer eigenständigen .exe bündeln (einmalig auf einem
Windows-Rechner mit Python auszuführen):

        python
        pip install pyinstaller oletools
        pyinstaller --onefile --console --name VbaExtractor VbaExtractor.py

Die fertige Datei liegt danach unter: dist\VbaExtractor.exe
Diese .exe kann anschließend auf beliebige andere Windows-Systeme kopiert
werden und läuft dort ohne weitere Installation.
================================================================================
"""

import os
import sys
import re
from datetime import datetime
from oletools.olevba import VBA_Parser

# ==============================================================================
#  FUNKTION 1: VBA aus .swp extrahieren und in .txt speichern
# ==============================================================================
def process_swp_file(swp_path, output_txt_path):
    """Extrahiert VBA-Code aus einer .swp Datei und speichert ihn in einer .txt Datei."""
    try:
        vbaparser = VBA_Parser(swp_path)
        border = "=" * 80 
        
        with open(output_txt_path, 'w', encoding='utf-8') as out_file:
            out_file.write(f"--- VBA-Export aus: {os.path.basename(swp_path)} ---\n\n")
            
            for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                # P-Code-Dump herausfiltern
                if vba_filename == 'VBA_P-code.txt':
                    continue
                
                out_file.write(" " + border + "\n")
                out_file.write(f"  >> MODUL: {vba_filename}\n")
                out_file.write(" " + border + "\n\n")
                out_file.write(vba_code)
                out_file.write("\n\n")
                
        vbaparser.close()
        print(f"[OK] .swp exportiert: {os.path.basename(output_txt_path)}")
        
    except Exception as e:
        print(f"[FEHLER] Fehler bei {swp_path}: {e}")

# ==============================================================================
#  FUNKTION 2: Module aus .txt rekonstruieren und in Ordner speichern
# ==============================================================================
def extract_from_txt(txt_path):
    """Parst die exportierte .txt-Datei und speichert die Module als Einzeldateien."""
    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Ordnername: YYYY-MM-DD_HH-MM_Dateiname
    folder_name = f"{timestamp}_{base_name}"
    output_dir = os.path.join(os.path.dirname(txt_path), folder_name)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[FEHLER] Konnte {txt_path} nicht lesen: {e}")
        return
        
    # Regex sucht nach den Modul-Headern
    pattern = re.compile(r'^\s*>> MODUL:\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    
    if not matches:
        print(f"[INFO] Keine Module in '{os.path.basename(txt_path)}' gefunden.")
        return
        
    print(f"Starte Rekonstruktion in Ordner: {folder_name}")
    
    for i, match in enumerate(matches):
        module_name = match.group(1).strip()
        
        # Falls das Modul keine Endung hat (z.B. Standardmodule), fügen wir .bas hinzu
        if not os.path.splitext(module_name)[1]:
            module_name += ".bas"
            
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        raw_block = content[start_idx:end_idx]
        
        # Den Header (Trennlinie nach dem Modulnamen) entfernen
        header_pattern = r'^\s*={10,}\s*\n+'
        cleaned_code = re.sub(header_pattern, '', raw_block, count=1)
        
        # Überflüssige Leerzeilen am Ende entfernen
        cleaned_code = cleaned_code.rstrip('\n')
        
        # Modul-Datei schreiben
        out_file_path = os.path.join(output_dir, module_name)
        try:
            with open(out_file_path, 'w', encoding='utf-8') as out_f:
                out_f.write(cleaned_code + '\n')
            print(f"  [OK] {module_name} wiederhergestellt.")
        except Exception as e:
            print(f"  [FEHLER] Konnte {module_name} nicht schreiben: {e}")
            
    print(f"[FERTIG] {len(matches)} Module erfolgreich rekonstruiert.")

# ==============================================================================
#  HAUPTPROGRAMM (Drag & Drop Logik)
# ==============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Nutzung:")
        print("  - Ziehe eine .swp Datei auf dieses Skript, um sie in .txt umzuwandeln.")
        print("  - Ziehe eine .txt Datei auf dieses Skript, um die Module zu rekonstruieren.")
        input("\nDrücke Enter zum Beenden...")
        sys.exit(1)

    # Über alle Dateien iterieren, die auf das Skript gezogen wurden
    for input_path in sys.argv[1:]:
        ext = os.path.splitext(input_path)[1].lower()
        
        if ext == '.swp':
            txt_path = os.path.splitext(input_path)[0] + ".txt"
            print(f"\nVerarbeite SWP-Export: {os.path.basename(input_path)}")
            process_swp_file(input_path, txt_path)
            
        elif ext == '.txt':
            print(f"\nVerarbeite TXT-Rekonstruktion: {os.path.basename(input_path)}")
            extract_from_txt(input_path)
            
        else:
            print(f"\n[UNBEKANNT] Dateityp '{ext}' wird nicht unterstützt: {os.path.basename(input_path)}")
            
    # Hält das Konsolenfenster offen, damit man das Ergebnis nach dem Drag & Drop lesen kann
    print("\nAlle Vorgänge abgeschlossen.")
    input("Drücke Enter zum Beenden...")