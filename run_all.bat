@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel% neq 0 (
  echo [Cognira BTI][ERROR] Python is required but was not found in PATH.
  pause
  exit /b 1
)
python run_all.py %*
pause
