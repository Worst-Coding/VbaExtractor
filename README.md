# VbaExtractor

A two-way tool for handling VBA macros in `.swp` files (e.g. SolidWorks Macros).

## What this script does
 
`VbaExtractor` was built to consolidate VBA macros from `.swp` files into a single text file, so the code can easily be handed to an LLM for further work and afterwards reconstructed back into individual module files.
 
It supports two conversion directions:
 
1. **`.swp` → `.txt`**
   Extracts the VBA code contained in a `.swp` file and saves all modules together in one readable `.txt` file.
2. **`.txt` → folder of individual files**
   Reconstructs the individual VBA modules from a previously exported `.txt` file as separate files (`.bas`, `.cls`, `.frm`, ...) inside a new folder named with the current date/time.
The file extension of the input determines which operation runs automatically — so the same `.py` file (or `.exe`) can be used for both directions.

## Requirements

- Python 3.8 or newer
- The Python package [`oletools`](https://pypi.org/project/oletools/)

## Installation

1. Install Python (if not already installed): [python.org/downloads](https://www.python.org/downloads/)
   On Windows, make sure to enable the **"Add Python to PATH"** option in the installer.

2. Install the required package. Open the Command Prompt (cmd) and run:

   ```bash
   pip install oletools
   ```

3. Clone this repository or download `VbaExtractor.py`.

## Usage

### Drag & Drop (Windows)

Simply drag one or more `.swp` or `.txt` files onto `VbaExtractor.py` (or the compiled `.exe`). The script opens a console window, processes all provided files one by one, and waits for Enter at the end.

### From the command line

```bash
python VbaExtractor.py "C:\path\to\file.swp"
python VbaExtractor.py "C:\path\to\file.txt"
```

Multiple files can also be passed at once:

```bash
python VbaExtractor.py file1.swp file2.swp modules_export.txt
```

## Building a standalone .exe (no Python installation required)

To distribute the tool without requiring a separate Python installation, it can be bundled into a standalone `.exe` using [PyInstaller](https://pyinstaller.org/). This needs to be done once on a Windows machine that has Python installed:

```bash
pip install pyinstaller oletools
pyinstaller --onefile --console --name VbaExtractor VbaExtractor.py
```

The resulting file will be located at `dist\VbaExtractor.exe` and can then be copied to any other Windows system — it will run there without any further installation.

> **Note:** If the `.exe` crashes with a `ModuleNotFoundError`, this usually fixes it:
> ```bash
> pyinstaller --onefile --console --name VbaExtractor --hidden-import=olefile --hidden-import=oletools.olevba VbaExtractor.py
> ```

## Example output

Exporting a `.swp` file produces a `.txt` file that looks roughly like this:

```
--- VBA export from: Template.swp ---

 ================================================================================
  >> MODULE: Module1.bas
 ================================================================================

Sub Example()
    MsgBox "Hello World"
End Sub
```

Reconstructing that `.txt` file produces a folder like:

```
YYYY-MM-DD_HH-MM_Template/
└── Module1.bas
```

## License

This project is licensed under the [MIT License](LICENSE).
