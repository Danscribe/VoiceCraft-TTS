@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cls

:: ============================================================
:: VoiceCraft TTS — Offline Voice Pack Downloader
:: Run this ONCE on a PC with internet to download all voices.
:: It creates a "VoiceCraft_Voices.zip" you can copy to offline PCs.
:: ============================================================

echo.
echo    ╔══════════════════════════════════════════════════════╗
echo    ║     VoiceCraft TTS — Voice Pack Downloader          ║
echo    ║  Downloads 30 essential Piper voices for offline    ║
echo    ╚══════════════════════════════════════════════════════╝
echo.

set "VOICE_DIR=%USERPROFILE%\.voicecraft_tts\piper_voices"
set "OUTPUT_ZIP=%CD%\VoiceCraft_Voices.zip"
set "TEMP_LIST=%TEMP%\voicecraft_urls.txt"

:: Ensure voice cache directory exists
if not exist "%VOICE_DIR%" mkdir "%VOICE_DIR%"

:: Python check
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/3] Installing Python packages if needed...
python -m pip install requests tqdm -q

echo.
echo [2/3] Downloading 30 essential Piper voices...
echo    This will take 5-10 minutes depending on your internet speed.
echo    Voice cache location: %VOICE_DIR%
echo.

python -c "
import sys, os, urllib.request, json, time
from pathlib import Path

VOICE_DIR = Path(os.path.expanduser('~')) / '.voicecraft_tts' / 'piper_voices'
VOICE_DIR.mkdir(parents=True, exist_ok=True)

HF_BASE = 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0'

ESSENTIAL_VOICES = [
    'en_US-amy-medium', 'en_US-ryan-high', 'en_US-lessac-high', 'en_US-libritts-high', 'en_US-joe-medium',
    'en_GB-cori-high', 'en_GB-alan-medium', 'en_GB-southern_english_female-medium',
    'en_AU-natasha-medium', 'en_CA-claire-medium',
    'es_ES-carlfm-x_low', 'es_MX-ald-medium',
    'fr_FR-siwis-medium', 'fr_FR-tom-medium',
    'de_DE-thorsten-high', 'de_DE-eva_k-medium',
    'it_IT-paola-medium', 'pt_BR-faber-medium', 'pt_PT-tugão-medium',
    'ru_RU-irina-medium', 'zh_CN-huayan-medium', 'ja_JP-0amazon-medium',
    'ko_KO-0gihun-medium', 'ar_JO-kareem-medium', 'hi_IN-cmu_indic_medium',
    'nl_NL-thijs-medium', 'pl_PL-gosia-medium', 'tr_TR-fahrettin-medium',
    'sv_SE-nst-medium', 'en_US-hfc_female', 'en_US-hfc_male'
]

def download_voice(voice_id):
    parts = voice_id.split('-')
    if len(parts) < 2:
        return False
    lang = parts[0]
    quality = 'medium'
    if '-low' in voice_id: quality = 'low'
    elif '-high' in voice_id: quality = 'high'
    elif '-x_low' in voice_id: quality = 'x_low'
    
    voice_name = voice_id.replace(f'{lang}-', '').replace(f'-{quality}', '')
    url_base = f'{HF_BASE}/{lang}/{voice_name}/{quality}'
    
    model_name = f'{voice_id}.onnx'
    config_name = f'{voice_id}.onnx.json'
    model_path = VOICE_DIR / model_name
    config_path = VOICE_DIR / config_name
    
    success = True
    for fname, url_suffix in [(model_name, model_name), (config_name, config_name)]:
        fpath = VOICE_DIR / fname
        if fpath.exists():
            print(f'  [SKIP] {fname} already exists')
            continue
        url = f'{url_base}/{url_suffix}'
        try:
            print(f'  [DOWNLOAD] {fname} ...', end=' ', flush=True)
            urllib.request.urlretrieve(url, fpath)
            print('OK')
        except Exception as e:
            print(f'FAIL ({e})')
            success = False
    return success

print(f'Downloading to: {VOICE_DIR}')
print(f'Total voices: {len(ESSENTIAL_VOICES)}')
print()

ok = 0
fail = 0
for i, vid in enumerate(ESSENTIAL_VOICES, 1):
    print(f'[{i}/{len(ESSENTIAL_VOICES)}] {vid}')
    if download_voice(vid):
        ok += 1
    else:
        fail += 1
    print()

print('='*60)
print(f'DONE: {ok} voices ready, {fail} failed.')
print(f'Location: {VOICE_DIR}')
print('='*60)
"

if errorlevel 1 (
    echo [ERROR] Voice download failed. Check your internet connection.
    pause
    exit /b 1
)

echo.
echo [3/3] Creating Voice Pack ZIP for offline transfer...

:: Create ZIP using PowerShell
powershell -Command "& { $source = '%VOICE_DIR%'; $dest = '%OUTPUT_ZIP%'; if (Test-Path $dest) { Remove-Item $dest }; Add-Type -Assembly 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::CreateFromDirectory($source, $dest, 'Optimal', $false); Write-Host \"ZIP created: $dest\" }"

if exist "%OUTPUT_ZIP%" (
    echo.
    echo ═══════════════════════════════════════════════════════
    echo   SUCCESS! Voice Pack Ready for Offline Use
    echo ═══════════════════════════════════════════════════════
    echo.
    echo   Location: %OUTPUT_ZIP%
    echo.
    echo   HOW TO USE ON AN OFFLINE PC:
    echo   1. Copy this ZIP file to the offline PC (USB, email, etc.)
    echo   2. On the offline PC, extract the ZIP to:
    echo      C:\Users\[YourName]\.voicecraft_tts\piper_voices\
    echo   3. Launch VoiceCraft_TTS.exe — all voices will work offline!
    echo.
    echo   OR — run the included 'install_voices.bat' (if you create one)
    echo   OR — double-click the ZIP and drag files to the folder above.
    echo.
    echo   You can also distribute this ZIP alongside VoiceCraft_TTS.exe
    echo   so your users have everything they need.
    echo.
    echo   Approximate ZIP size: 150-300 MB (30 voices)
    echo ═══════════════════════════════════════════════════════
) else (
    echo [ERROR] Failed to create ZIP.
)

echo.
pause
