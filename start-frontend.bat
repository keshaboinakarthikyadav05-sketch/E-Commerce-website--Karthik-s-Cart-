@echo off
echo ========================================================
echo         STARTING SHOPORA REACT FRONTEND (PORT 3000)
echo ========================================================
cd /d "%~dp0frontend"
call npm run dev
pause
