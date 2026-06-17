#!/usr/bin/env python3
"""VoiceCraft TTS - Entry point."""
import sys
import os

# Ensure the project root is on path when frozen by PyInstaller
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

if bundle_dir not in sys.path:
    sys.path.insert(0, bundle_dir)

from ui.main_app import VoiceCraftApp

def main():
    app = VoiceCraftApp()
    app.mainloop()

if __name__ == "__main__":
    main()
