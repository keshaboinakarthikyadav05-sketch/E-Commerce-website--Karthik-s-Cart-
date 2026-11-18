@echo off
title Launch SHOPORA Full-Stack
echo ========================================================
echo         LAUNCHING SHOPORA FULL-STACK PLATFORM
echo ========================================================
echo Starting Backend API on http://localhost:5000 ...
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    start "SHOPORA Backend (Port 5000)" cmd /k "cd /d %~dp0backend && "%LOCALAPPDATA%\Python\bin\python.exe" run.py"
) else (
    start "SHOPORA Backend (Port 5000)" cmd /k "cd /d %~dp0backend && python run.py"
)

timeout /t 2 /nobreak >nul

echo Starting React + Vite Frontend on http://localhost:3000 ...
start "SHOPORA Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo ========================================================
echo SHOPORA is now running!
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo Admin Demo: admin@shopora.com / Admin@123
echo Customer Demo: customer@shopora.com / Customer@123
echo ========================================================
pause
