"""
================================================================================
 VbaExtractor
================================================================================

WHAT THIS SCRIPT DOES
--------------------------------------------------------------------------------
VbaExtractor is a two-way tool for handling VBA macros in .swp files:

  1) .swp  ->  .txt
     Extracts the VBA code contained in a .swp file and saves all modules
     together in one readable .txt file.

  2) .txt  ->  folder of individual files
     Takes a previously exported .txt file and reconstructs the individual
     VBA modules as separate files (.bas, .cls, .frm, ...) inside a new
     folder named with the current date/time.

USAGE (Drag & Drop)
--------------------------------------------------------------------------------
Simply drag one or more .swp or .txt files onto the script. The script
automatically detects which operation to run based on the file extension.

REQUIREMENTS
--------------------------------------------------------------------------------
- Python 3.8 or newer
- The Python package "oletools"

INSTALLATION
--------------------------------------------------------------------------------
1) Install Python (if not already installed):
   https://www.python.org/downloads/
   IMPORTANT: On Windows, enable the "Add Python to PATH" option
   in the installer.

2) Install the required package. Open the Command Prompt (cmd) and run:

        pip install oletools

3) Run the script, e.g. by dragging a .swp or .txt file onto
   VbaExtractor.py, or via the console:

       python VbaExtractor.py "C:\path\to\file.swp"

BUILDING A STANDALONE .EXE (no Python installation required)
--------------------------------------------------------------------------------
To distribute the script without requiring a separate Python installation, it
can be bundled into a standalone .exe using PyInstaller (run once on a
Windows machine that has Python installed):

        pip install pyinstaller oletools
        pyinstaller --onefile --console --name VbaExtractor VbaExtractor.py

The resulting file will be located at: dist\VbaExtractor.exe
This .exe can then be copied to any other Windows system and will run there
without any further installation.
================================================================================
"""

import os
import sys
import re
from datetime import datetime
from oletools.olevba import VBA_Parser

# ==============================================================================
#  FUNCTION 1: Extract VBA from .swp and save it as .txt
# ==============================================================================
def process_swp_file(swp_path, output_txt_path):
    """Extracts VBA code from a .swp file and saves it into a .txt file."""
    try:
        vbaparser = VBA_Parser(swp_path)
        border = "=" * 80 
        
        with open(output_txt_path, 'w', encoding='utf-8') as out_file:
            out_file.write(f"--- VBA export from: {os.path.basename(swp_path)} ---\n\n")
            
            for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                # Filter out the P-code dump
                if vba_filename == 'VBA_P-code.txt':
                    continue
                
                out_file.write(" " + border + "\n")
                out_file.write(f"  >> MODULE: {vba_filename}\n")
                out_file.write(" " + border + "\n\n")
                out_file.write(vba_code)
                out_file.write("\n\n")
                
        vbaparser.close()
        print(f"[OK] .swp exported: {os.path.basename(output_txt_path)}")
        
    except Exception as e:
        print(f"[ERROR] Error processing {swp_path}: {e}")

# ==============================================================================
#  FUNCTION 2: Reconstruct modules from .txt and save them in a folder
# ==============================================================================
def extract_from_txt(txt_path):
    """Parses the exported .txt file and saves the modules as individual files."""
    base_name = os.path.splitext(os.path.basename(txt_path))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Folder name: YYYY-MM-DD_HH-MM_filename
    folder_name = f"{timestamp}_{base_name}"
    output_dir = os.path.join(os.path.dirname(txt_path), folder_name)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read {txt_path}: {e}")
        return
        
    # Regex looks for the module headers
    pattern = re.compile(r'^\s*>> MODULE:\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))
    
    if not matches:
        print(f"[INFO] No modules found in '{os.path.basename(txt_path)}'.")
        return
        
    print(f"Starting reconstruction in folder: {folder_name}")
    
    for i, match in enumerate(matches):
        module_name = match.group(1).strip()
        
        # If the module has no extension (e.g. standard modules), add .bas
        if not os.path.splitext(module_name)[1]:
            module_name += ".bas"
            
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        raw_block = content[start_idx:end_idx]
        
        # Remove the header (separator line after the module name)
        header_pattern = r'^\s*={10,}\s*\n+'
        cleaned_code = re.sub(header_pattern, '', raw_block, count=1)
        
        # Remove trailing blank lines
        cleaned_code = cleaned_code.rstrip('\n')
        
        # Write the module file
        out_file_path = os.path.join(output_dir, module_name)
        try:
            with open(out_file_path, 'w', encoding='utf-8') as out_f:
                out_f.write(cleaned_code + '\n')
            print(f"  [OK] {module_name} restored.")
        except Exception as e:
            print(f"  [ERROR] Could not write {module_name}: {e}")
            
    print(f"[DONE] {len(matches)} modules successfully reconstructed.")

# ==============================================================================
#  MAIN PROGRAM (Drag & Drop logic)
# ==============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  - Drag a .swp file onto this script to convert it to .txt.")
        print("  - Drag a .txt file onto this script to reconstruct the modules.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Iterate over all files that were dragged onto the script
    for input_path in sys.argv[1:]:
        ext = os.path.splitext(input_path)[1].lower()
        
        if ext == '.swp':
            txt_path = os.path.splitext(input_path)[0] + ".txt"
            print(f"\nProcessing SWP export: {os.path.basename(input_path)}")
            process_swp_file(input_path, txt_path)
            
        elif ext == '.txt':
            print(f"\nProcessing TXT reconstruction: {os.path.basename(input_path)}")
            extract_from_txt(input_path)
            
        else:
            print(f"\n[UNKNOWN] File type '{ext}' is not supported: {os.path.basename(input_path)}")
            
    # Keep the console window open so the result can be read after Drag & Drop
    print("\nAll operations completed.")
    input("Press Enter to exit...")
