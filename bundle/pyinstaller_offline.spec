# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for VoiceCraft TTS (offline-ready bundle).
Includes bundled Piper voices so the app works without internet.
"""
import sys
import os
from pathlib import Path
import customtkinter

ctk_path = Path(customtkinter.__file__).parent
project_root = Path(SPECPATH).parent
voice_cache = Path.home() / ".voicecraft_tts" / "piper_voices"

# Collect voices if available
voice_data = []
if voice_cache.exists():
    for f in voice_cache.rglob("*"):
        if f.is_file():
            rel = f.relative_to(voice_cache)
            voice_data.append((str(f), str(Path("piper_voices") / rel)))

a = Analysis(
    [str(project_root / 'main.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(ctk_path / 'assets' / 'themes'), 'customtkinter/assets/themes'),
        (str(project_root / 'config'), 'config'),
        (str(project_root / 'tts'), 'tts'),
        (str(project_root / 'ui'), 'ui'),
    ] + voice_data,
    hiddenimports=[
        'customtkinter',
        'piper',
        'onnxruntime',
        'soundfile',
        'pydub',
        'pygame',
        'requests',
        'PIL',
        'pyperclip',
        'config.settings',
        'config.voice_data',
        'tts.piper_engine',
        'tts.api_providers',
        'tts.audio_player',
        'ui.main_app',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoiceCraft_TTS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'assets' / 'icon.ico') if (project_root / 'assets' / 'icon.ico').exists() else None,
)
