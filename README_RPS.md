# Rock Paper Scissors

Simple CLI Rock-Paper-Scissors game.

Usage
-----

Run the game with Python (from project root):

```powershell
python rock_paper_scissors.py
```

Type one of: `rock`/`r`, `paper`/`p`, `scissors`/`s`.
Type `quit` (or Ctrl+C) to exit.

The program will show each round's result and keep a running score for you and the computer.

GUI
---

There's a simple Tkinter GUI available as `rps_gui.py` in this folder. To run it:

```powershell
python rps_gui.py
```

The GUI shows small icon-like drawings for each move, a status line, score, and buttons. It also supports keyboard shortcuts: `r`, `p`, `s`.

Optional sound
--------------

On Windows, the GUI will play short beeps for wins/loses/ties using the built-in `winsound` API. No extra dependencies are required for the sound. On other platforms the sound is skipped.

Build an executable (optional)
----------------------------

You can create a single-file Windows executable using PyInstaller. From this folder, install PyInstaller and run the build script provided:

```powershell
# install pyinstaller once
pip install pyinstaller

# run the build script (this calls pyinstaller --onefile rps_gui.py)
.\build_exe.ps1
```

The produced exe will be in `dist\rps_gui.exe` when the build finishes.
