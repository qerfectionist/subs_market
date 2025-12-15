@echo off
REM Launcher for Subscription Bot
REM Ensures correct Python venv is used and module path is set

echo Starting Bot...
echo Python: ..\.venv\Scripts\python.exe
echo Working Directory: %CD%

REM Check if venv exists
if not exist "..\.venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found at ..\.venv
    echo Please create it first.
    pause
    exit /b
)

REM Run as module to fix import paths
..\.venv\Scripts\python -m src.ui.telegram.main

echo.
echo Bot stopped.
pause
