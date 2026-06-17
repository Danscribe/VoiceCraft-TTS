"""Build script to compile VoiceCraft to a single .exe."""
import PyInstaller.__main__
import os
import customtkinter

ctk_path = os.path.dirname(customtkinter.__file__)

PyInstaller.__main__.run([
    'main.py',
    '--name=VoiceCraft_TTS',
    '--onefile',
    '--windowed',
    '--icon=assets/icon.ico',
    f'--add-data={ctk_path}/assets/themes;customtkinter/assets/themes',
    f'--add-data={ctk_path};customtkinter',
    '--hidden-import=piper',
    '--hidden-import=onnxruntime',
    '--hidden-import=soundfile',
    '--hidden-import=pydub',
    '--hidden-import=pygame',
    '--hidden-import=requests',
    '--hidden-import=PIL',
    '--hidden-import=pyperclip',
    '--collect-data=customtkinter',
    '--clean',
    '-y'
])
