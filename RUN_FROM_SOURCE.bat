@echo off
echo.
echo ================================================
echo  VoiceCraft TTS — Quick Source Launcher
echo ================================================
echo.
echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install from https://python.org
    pause
    exit /b 1
)

echo Installing dependencies (if needed)...
python -m pip install -r requirements.txt

echo.
echo Launching VoiceCraft...
python main.py
pause
