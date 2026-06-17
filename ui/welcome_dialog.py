"""First-run welcome dialog for offline installer users."""
import customtkinter as ctk
from pathlib import Path
import sys
from config.settings import ConfigManager

class WelcomeDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Welcome to VoiceCraft TTS")
        self.geometry("560x420")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        frame.grid_columnconfigure(0, weight=1)
        
        # Header
        ctk.CTkLabel(frame, text="🎙 VoiceCraft TTS", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(0, 5))
        ctk.CTkLabel(frame, text="300+ AI Voices — Ready Offline", font=ctk.CTkFont(size=14), text_color="gray").grid(row=1, column=0, pady=(0, 20))
        
        # Offline status
        bundled = self._count_bundled_voices()
        try:
            from tts.sapi_engine import get_system_voices
            sapi_count = len(get_system_voices())
        except Exception:
            sapi_count = 0
        
        if bundled > 0 or sapi_count > 0:
            status_text = f"✅ {sapi_count} Windows voices + {bundled} bundled voices ready instantly!"
            status_color = "#00a8e8"
        else:
            status_text = "ℹ️ No bundled voices found. You can download voices from the sidebar."
            status_color = "gray"
        
        ctk.CTkLabel(frame, text=status_text, font=ctk.CTkFont(size=13, weight="bold"), text_color=status_color).grid(row=2, column=0, pady=(0, 15))
        
        # Info boxes
        info_frame = ctk.CTkFrame(frame)
        info_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkLabel(info_frame, text="🏠 Windows Voices", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 5))
        ctk.CTkLabel(info_frame, text="Built-in voices that work instantly.\nNo download, no internet needed.", font=ctk.CTkFont(size=12), wraplength=180).grid(row=1, column=0, padx=10, pady=(0, 10))
        
        ctk.CTkLabel(info_frame, text="🆓 Offline Voices", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=(10, 5))
        ctk.CTkLabel(info_frame, text="Piper voices work without internet.\nSelect any 🆓 or ✅ voice in the sidebar.", font=ctk.CTkFont(size=12), wraplength=180).grid(row=1, column=1, padx=10, pady=(0, 10))
        
        ctk.CTkLabel(info_frame, text="☁ Cloud Voices", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=(10, 5))
        ctk.CTkLabel(info_frame, text="Deepgram, Fish Audio, TopMedia AI.\nAdd API keys in Settings → API Keys.", font=ctk.CTkFont(size=12), wraplength=180).grid(row=1, column=2, padx=10, pady=(0, 10))
        
        # Quick tips
        ctk.CTkLabel(frame, text="Quick Tips", font=ctk.CTkFont(size=14, weight="bold")).grid(row=4, column=0, pady=(10, 5), sticky="w")
        tips = [
            "1. Type your text in the main box and click 'Generate Speech'.",
            "2. Use the mood controls to change speed, pitch, and emotion.",
            "3. Click 'Download' to save your audio as MP3/WAV/OGG/FLAC.",
            "4. Favorites and recent texts are saved automatically.",
        ]
        for i, tip in enumerate(tips):
            ctk.CTkLabel(frame, text=tip, font=ctk.CTkFont(size=12), wraplength=500, justify="left").grid(row=5+i, column=0, sticky="w", pady=2)
        
        # Checkbox
        self.dont_show = ctk.CTkCheckBox(frame, text="Don't show this again")
        self.dont_show.grid(row=9, column=0, pady=(15, 5), sticky="w")
        
        # Close button
        ctk.CTkButton(frame, text="Get Started", font=ctk.CTkFont(size=14, weight="bold"), height=40,
                     command=self.close).grid(row=10, column=0, pady=(10, 0), sticky="ew")
        
        self.wait_window(self)
    
    def _count_bundled_voices(self) -> int:
        try:
            from tts.piper_engine import _get_bundle_dir
            bundle = _get_bundle_dir()
            if not bundle:
                return 0
            return len(list(bundle.glob("*.onnx")))
        except Exception:
            return 0
    
    def close(self):
        if self.dont_show.get():
            ConfigManager().set("welcome_shown", True)
        self.destroy()

def maybe_show_welcome(parent):
    cfg = ConfigManager()
    if not cfg.get("welcome_shown", False):
        WelcomeDialog(parent)
