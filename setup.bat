@echo off
echo ========================================================
echo       SHOPORA E-COMMERCE - ONE-CLICK INSTALL & SETUP
echo ========================================================
echo.

set PYTHON_CMD=python
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Python\bin\python.exe"
)

echo [1/3] Verifying Python Backend Dependencies...
%PYTHON_CMD% -m pip install -r "%~dp0backend\requirements.txt"

echo.
echo [2/3] Seeding 100+ Products into PostgreSQL...
cd /d "%~dp0backend"
%PYTHON_CMD% -m seed.seed_data
cd /d "%~dp0"

echo.
echo [3/3] Installing Frontend Packages...
cd /d "%~dp0frontend"
call npm install
cd /d "%~dp0"

echo.
echo ========================================================
echo  Setup Completed Successfully!
echo  To start the application:
echo    1. Double-click start-backend.bat (Port 5000)
echo    2. Double-click start-frontend.bat (Port 3000)
echo    3. Open http://localhost:3000 in your browser!
echo ========================================================
pause
