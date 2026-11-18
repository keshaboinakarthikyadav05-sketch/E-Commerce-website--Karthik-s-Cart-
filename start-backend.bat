@echo off
echo ========================================================
echo         STARTING SHOPORA FLASK BACKEND API (PORT 5000)
echo ========================================================
cd /d "%~dp0backend"
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    "%LOCALAPPDATA%\Python\bin\python.exe" run.py
) else (
    python run.py
)
pause
