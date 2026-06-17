@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cls

:: ============================================================
:: VoiceCraft TTS — Offline Voice Pack Installer
:: Run this on the OFFLINE PC to install voices from the ZIP.
:: ============================================================

echo.
echo    ╔══════════════════════════════════════════════════════╗
echo    ║   VoiceCraft TTS — Offline Voice Pack Installer    ║
echo    ╚══════════════════════════════════════════════════════╝
echo.

set "VOICE_DIR=%USERPROFILE%\.voicecraft_tts\piper_voices"
set "SOURCE_ZIP=%~dp0VoiceCraft_Voices.zip"

:: Check if ZIP exists in same folder
if not exist "%SOURCE_ZIP%" (
    echo [INFO] Looking for VoiceCraft_Voices.zip in the current folder...
    echo        %SOURCE_ZIP%
    echo.
    echo [NOT FOUND] Please place VoiceCraft_Voices.zip in the same folder as this script.
    echo.
    echo Alternative: Extract the ZIP manually to:
    echo    %VOICE_DIR%
    echo.
    pause
    exit /b 1
)

echo [1/2] Creating voice cache directory...
if not exist "%VOICE_DIR%" mkdir "%VOICE_DIR%"

echo.
echo [2/2] Extracting voices to cache...
powershell -Command "& { $zip = '%SOURCE_ZIP%'; $dest = '%VOICE_DIR%'; Add-Type -Assembly 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::ExtractToDirectory($zip, $dest, $true); Write-Host 'Extraction complete.' }"

if errorlevel 1 (
    echo [ERROR] Extraction failed. Make sure the ZIP is not corrupted.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════
echo   SUCCESS! Voices installed for offline use.
echo ═══════════════════════════════════════════════════════
echo.
echo   Location: %VOICE_DIR%
echo.
echo   You can now launch VoiceCraft_TTS.exe and use any
echo   voice with the (checkmark) or (free) icon completely offline.
echo.
echo   Note: If you already have the app open, close and reopen it
echo   to refresh the voice list.
echo.
pause
