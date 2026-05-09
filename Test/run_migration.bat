@echo off
cd /d "E:\PROJECTS\Transport"
echo Clearing Python cache...
rmdir /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo Running migration...
python migrate_vendor_addresses.py
echo.
echo Migration complete. Press any key to exit...
pause >nul
