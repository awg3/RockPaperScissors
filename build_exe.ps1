# Build a single-file executable for rps_gui.py using PyInstaller
# Run this from PowerShell in the rockPaperScissors folder.

# Ensure PyInstaller is installed
pip install pyinstaller

# Remove previous build/dist
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path dist) { Remove-Item -Recurse -Force dist }

# Build one-file executable
pyinstaller --onefile --noconsole rps_gui.py --name rps_gui

Write-Host "Build finished. Check the dist\rps_gui.exe file." -ForegroundColor Green
