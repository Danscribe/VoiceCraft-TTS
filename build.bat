@echo off
echo Building VoiceCraft TTS...
pyinstaller main.py --name=VoiceCraft_TTS --onefile --windowed --clean -y --add-data "%PYTHON_PATH%\Lib\site-packages\customtkinter;customtkinter" --hidden-import=piper --hidden-import=onnxruntime --hidden-import=soundfile --hidden-import=pydub --hidden-import=pygame --hidden-import=requests --hidden-import=PIL --hidden-import=pyperclip --hidden-import=customtkinter
echo Build complete! Check the 'dist' folder.
pause
