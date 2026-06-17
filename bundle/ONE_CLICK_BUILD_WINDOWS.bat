@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cls

:: ============================================================
:: VoiceCraft TTS — One-Click Windows Builder
:: This script:
::   1. Checks for Python (auto-installs if missing)
::   2. Installs all dependencies
::   3. Downloads offline voice pack (30+ voices)
::   4. Builds the .exe with PyInstaller
::   5. Creates a professional Inno Setup installer
::   6. Outputs a final Setup.exe ready to distribute
:: ============================================================

echo.
echo    ╔══════════════════════════════════════════════════════╗
echo    ║          VoiceCraft TTS — Windows Builder            ║
echo    ║         (One-click offline-ready installer)          ║
echo    ╚══════════════════════════════════════════════════════╝
echo.

set "PROJECT_ROOT=%~dp0.."
set "BUILD_DIR=%PROJECT_ROOT%\build_bundle"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "VOICE_CACHE=%USERPROFILE%\.voicecraft_tts\piper_voices"
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

:: Check / Install Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [1/6] Python not found. Downloading Python 3.11...
    curl -L -o "%TEMP%\python_installer.exe" "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
    echo [1/6] Installing Python (silent)...
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    refreshenv >nul 2>&1
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python installation failed. Please install manually from python.org.
        pause
        exit /b 1
    )
)
for /f "tokens=*" %%a in ('python --version') do echo [1/6] Python OK: %%a

:: Install dependencies
echo [2/6] Installing dependencies (this may take a few minutes)...
cd /d "%PROJECT_ROOT%"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install pyinstaller

:: Download offline voice pack
echo [3/6] Downloading offline voice pack (30 essential voices for offline use)...
python bundle\prepare_offline_voices.py
if errorlevel 1 (
    echo WARNING: Some voices failed to download, but we'll continue...
)

:: Build .exe with PyInstaller
echo [4/6] Building executable with PyInstaller...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%BUILD_DIR%"
mkdir "%DIST_DIR%"

:: Build main .exe
pyinstaller bundle\pyinstaller_offline.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

:: Copy bundled voices into build tree
echo [5/6] Bundling offline voices into installer payload...
if exist "%VOICE_CACHE%" (
    mkdir "%DIST_DIR%\VoiceCraft_TTS\voices" 2>nul
    xcopy /s /e /i /y "%VOICE_CACHE%\*" "%DIST_DIR%\VoiceCraft_TTS\voices\" >nul
    echo        Bundled %VOICE_CACHE% into installer.
)

:: Copy license / readme
if exist "%PROJECT_ROOT%\README.md" copy /y "%PROJECT_ROOT%\README.md" "%DIST_DIR%\VoiceCraft_TTS\" >nul

:: Build Inno Setup installer
echo [6/6] Creating professional installer...
if exist "%INNO_PATH%" (
    "%INNO_PATH%" bundle\installer.iss
    if errorlevel 1 (
        echo WARNING: Inno Setup build failed, but portable .exe is ready in dist\VoiceCraft_TTS
    ) else (
        echo.
        echo ═══════════════════════════════════════════════════════
        echo   INSTALLER BUILD COMPLETE!
        echo ═══════════════════════════════════════════════════════
        echo.
        echo   Your installer is at:
        echo   %PROJECT_ROOT%\Output\VoiceCraft_Setup.exe
        echo.
        echo   This .exe will:
        echo   • Install VoiceCraft to Program Files
        echo   • Bundle 30+ offline voices (no internet needed)
        echo   • Create Desktop / Start Menu shortcuts
        echo   • Register for uninstall via Control Panel
        echo.
    )
) else (
    echo.
    echo Inno Setup 6 not found at default path.
    echo Download it from: https://jrsoftware.org/isdl.php
    echo.
    echo Portable .exe is ready at:
    echo %DIST_DIR%\VoiceCraft_TTS\VoiceCraft_TTS.exe
    echo.
    echo To make a Setup.exe, install Inno Setup and re-run this script.
    echo.
)

echo Press any key to exit...
pause >nul
endlocal
