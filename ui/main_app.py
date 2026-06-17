"""Main VoiceCraft TTS Application UI."""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import datetime
from pathlib import Path

from config.settings import ConfigManager
from config.voice_data import get_all_voices, get_voice_by_id, EMOTIONS, VOICE_CATEGORIES
from tts.audio_player import AudioPlayer
from tts.piper_engine import synthesize as piper_synthesize, download_voice, get_voice_path, _get_bundle_dir
from tts.api_providers import DeepgramProvider, FishAudioProvider, TopMediaProvider
from ui.welcome_dialog import maybe_show_welcome

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VoiceCraftApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VoiceCraft TTS - 300+ Voices")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        self.config_manager = ConfigManager()
        self.audio_player = AudioPlayer()
        self.current_output = None
        self.is_generating = False
        
        # Check which piper voices are bundled (offline-ready)
        self._bundled_voices = set()
        bundle_dir = _get_bundle_dir()
        if bundle_dir:
            for f in bundle_dir.glob("*.onnx"):
                self._bundled_voices.add(f.stem)
        
        # Providers
        self.providers = {
            "piper": None,
            "deepgram": DeepgramProvider(self.config_manager.get_api_key("deepgram")),
            "fish_audio": FishAudioProvider(self.config_manager.get_api_key("fish_audio")),
            "topmedia_ai": TopMediaProvider(self.config_manager.get_api_key("topmedia_ai"))
        }
        
        self.all_voices = get_all_voices()
        self.filtered_voices = self.all_voices.copy()
        
        self.build_ui()
        self.load_defaults()
        
        # Show welcome dialog on first run (after UI is ready)
        self.after(200, lambda: maybe_show_welcome(self))
    
    def build_ui(self):
        # ========== Grid layout ==========
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main
        self.grid_rowconfigure(0, weight=1)
        
        # ========== Sidebar ==========
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)
        self.sidebar.grid_propagate(False)
        
        # Title
        self.title_label = ctk.CTkLabel(self.sidebar, text="🎙 VoiceCraft", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.sidebar, text="300+ AI Voices", font=ctk.CTkFont(size=12), text_color="gray")
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15))
        
        # Provider filter
        self.provider_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.provider_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        
        ctk.CTkLabel(self.provider_frame, text="Provider", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.provider_var = ctk.StringVar(value="All")
        self.provider_menu = ctk.CTkOptionMenu(self.provider_frame, values=["All"] + list(VOICE_CATEGORIES.keys()),
                                              variable=self.provider_var, command=self.filter_voices)
        self.provider_menu.pack(fill="x")
        
        # Voice search
        self.search_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.search_frame.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.search_frame, text="Search Voices", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type to filter...")
        self.search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_voices())
        
        # Voice list
        self.voice_list = tk.Listbox(self.search_frame, bg="#2b2b2b", fg="white", selectbackground="#00a8e8",
                                      selectforeground="white", font=("Segoe UI", 11), borderwidth=0, highlightthickness=0)
        self.voice_list.grid(row=2, column=0, sticky="nsew")
        self.voice_list.bind("<<ListboxSelect>>", self.on_voice_select)
        
        scrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.voice_list.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.voice_list.config(yscrollcommand=scrollbar.set)
        
        self.search_frame.grid_rowconfigure(2, weight=1)
        
        # Voice info
        self.voice_info = ctk.CTkLabel(self.sidebar, text="Select a voice", font=ctk.CTkFont(size=11), text_color="gray")
        self.voice_info.grid(row=4, column=0, padx=20, pady=(10, 5))
        
        # Favorites button
        self.fav_btn = ctk.CTkButton(self.sidebar, text="⭐ Add to Favorites", command=self.toggle_favorite)
        self.fav_btn.grid(row=5, column=0, padx=20, pady=10)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(self.sidebar, text="⚙ API Keys & Settings", command=self.open_settings)
        self.settings_btn.grid(row=6, column=0, padx=20, pady=(5, 20))
        
        # ========== Main Content ==========
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Mood / Emotion Controls
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.controls_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        # Emotion
        ctk.CTkLabel(self.controls_frame, text="Emotion", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.emotion_var = ctk.StringVar(value="neutral")
        self.emotion_menu = ctk.CTkOptionMenu(self.controls_frame, values=EMOTIONS, variable=self.emotion_var, width=140)
        self.emotion_menu.grid(row=1, column=0, padx=10, pady=(0, 10))
        
        # Speed
        ctk.CTkLabel(self.controls_frame, text="Speed", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        self.speed_var = ctk.DoubleVar(value=1.0)
        self.speed_slider = ctk.CTkSlider(self.controls_frame, from_=0.5, to=2.0, number_of_steps=15, variable=self.speed_var, width=140)
        self.speed_slider.grid(row=1, column=1, padx=10, pady=(0, 10))
        self.speed_label = ctk.CTkLabel(self.controls_frame, text="1.0x", width=40)
        self.speed_label.grid(row=1, column=2, padx=0, pady=(0, 10), sticky="w")
        self.speed_slider.configure(command=lambda v: self.speed_label.configure(text=f"{v:.1f}x"))
        
        # Pitch
        ctk.CTkLabel(self.controls_frame, text="Pitch", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        self.pitch_var = ctk.DoubleVar(value=1.0)
        self.pitch_slider = ctk.CTkSlider(self.controls_frame, from_=0.5, to=2.0, number_of_steps=15, variable=self.pitch_var, width=140)
        self.pitch_slider.grid(row=1, column=3, padx=10, pady=(0, 10))
        self.pitch_label = ctk.CTkLabel(self.controls_frame, text="1.0x", width=40)
        self.pitch_label.grid(row=1, column=4, padx=0, pady=(0, 10), sticky="w")
        self.pitch_slider.configure(command=lambda v: self.pitch_label.configure(text=f"{v:.1f}x"))
        
        # Text Input
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.input_frame, text="Text to Speak", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.text_input = ctk.CTkTextbox(self.input_frame, font=ctk.CTkFont(family="Segoe UI", size=13), wrap="word")
        self.text_input.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.text_input.insert("0.0", "Welcome to VoiceCraft. Type something here and select a voice to generate human-like speech.")
        
        # Character count
        self.char_count = ctk.CTkLabel(self.input_frame, text="0 characters", font=ctk.CTkFont(size=11), text_color="gray")
        self.char_count.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="e")
        self.text_input.bind("<KeyRelease>", lambda e: self.update_char_count())
        self.text_input.bind("<ButtonRelease>", lambda e: self.update_char_count())
        
        # Action Buttons
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.generate_btn = ctk.CTkButton(self.actions_frame, text="🎙 Generate Speech", font=ctk.CTkFont(size=14, weight="bold"),
                                         height=45, command=self.generate_speech)
        self.generate_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.play_btn = ctk.CTkButton(self.actions_frame, text="▶ Play", font=ctk.CTkFont(size=14), height=45,
                                     command=self.toggle_play, state="disabled")
        self.play_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.download_btn = ctk.CTkButton(self.actions_frame, text="⬇ Download", font=ctk.CTkFont(size=14), height=45,
                                         command=self.download_audio, state="disabled")
        self.download_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.clear_btn = ctk.CTkButton(self.actions_frame, text="🗑 Clear", font=ctk.CTkFont(size=14), height=45,
                                        command=self.clear_text)
        self.clear_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self.main_frame, mode="indeterminate", height=6)
        self.progress.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.progress.set(0)
        self.progress.grid_remove()
        
        # Status
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.grid(row=4, column=0, sticky="w", pady=(5, 0))
        
        # Populate voice list
        self.filter_voices()
    
    def load_defaults(self):
        defaults = self.config_manager.get("mood_defaults", {})
        self.speed_var.set(defaults.get("speed", 1.0))
        self.pitch_var.set(defaults.get("pitch", 1.0))
        self.emotion_var.set(defaults.get("emotion", "neutral"))
        self.speed_label.configure(text=f"{self.speed_var.get():.1f}x")
        self.pitch_label.configure(text=f"{self.pitch_var.get():.1f}x")
        self.update_char_count()
        
        # Select default voice if exists
        default_voice = self.config_manager.get("default_voice")
        if default_voice:
            for i, v in enumerate(self.filtered_voices):
                if v["id"] == default_voice:
                    self.voice_list.selection_clear(0, "end")
                    self.voice_list.selection_set(i)
                    self.voice_list.see(i)
                    self.on_voice_select(None)
                    break
    
    def filter_voices(self, _=None):
        provider = self.provider_var.get()
        query = self.search_entry.get().lower()
        
        self.filtered_voices = []
        for v in self.all_voices:
            if provider != "All" and v.get("category") != provider:
                continue
            if query and query not in v["name"].lower() and query not in v["id"].lower():
                continue
            self.filtered_voices.append(v)
        
        self.voice_list.delete(0, "end")
        for v in self.filtered_voices:
            if v["provider"] == "piper":
                if v["id"] in self._bundled_voices:
                    tag = "✅"  # Bundled, ready offline
                elif get_voice_path(v["id"]):
                    tag = "🆓"  # Downloaded locally
                else:
                    tag = "⬇"  # Needs download
            else:
                tag = "☁"  # Cloud provider
            self.voice_list.insert("end", f"{tag} {v['name']}")
    
    def on_voice_select(self, event):
        selection = self.voice_list.curselection()
        if not selection:
            return
        voice = self.filtered_voices[selection[0]]
        info = f"{voice['name']} | {voice['lang'].upper()} | {voice['gender'].title()} | {voice['quality'].title()}"
        
        # Offline status indicator
        if voice["provider"] == "piper":
            if voice["id"] in self._bundled_voices:
                info += " | ✅ Bundled (Offline Ready)"
            elif get_voice_path(voice["id"]):
                info += " | 🆓 Downloaded"
            else:
                info += " | ⬇ Click Generate to download"
        else:
            info += " | ☁ Cloud (API key required)"
        
        self.voice_info.configure(text=info)
    
    def get_selected_voice(self):
        selection = self.voice_list.curselection()
        if not selection:
            return None
        return self.filtered_voices[selection[0]]
    
    def update_char_count(self):
        text = self.text_input.get("0.0", "end")
        count = len(text.strip())
        self.char_count.configure(text=f"{count} characters")
    
    def toggle_play(self):
        if self.audio_player.is_playing():
            self.audio_player.pause()
            self.play_btn.configure(text="▶ Resume")
        elif self.audio_player.is_paused():
            self.audio_player.resume()
            self.play_btn.configure(text="⏸ Pause")
        else:
            if self.current_output and os.path.exists(self.current_output):
                self.audio_player.play(self.current_output)
                self.play_btn.configure(text="⏸ Pause")
    
    def clear_text(self):
        self.text_input.delete("0.0", "end")
        self.update_char_count()
    
    def generate_speech(self):
        if self.is_generating:
            return
        
        voice = self.get_selected_voice()
        if not voice:
            messagebox.showwarning("No Voice Selected", "Please select a voice from the sidebar.")
            return
        
        text = self.text_input.get("0.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty Text", "Please enter some text to synthesize.")
            return
        
        self.is_generating = True
        self.generate_btn.configure(state="disabled", text="Generating...")
        self.progress.grid()
        self.progress.start()
        self.status_label.configure(text=f"Synthesizing with {voice['name']}...")
        
        thread = threading.Thread(target=self._synth_thread, args=(voice, text), daemon=True)
        thread.start()
    
    def _synth_thread(self, voice, text):
        try:
            output_dir = Path(self.config_manager.get("output_dir", str(Path.home() / "Documents" / "VoiceCraft_Audio")))
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = self.config_manager.get("output_format", "mp3")
            output_path = str(output_dir / f"voicecraft_{voice['id']}_{timestamp}.{ext}")
            
            speed = self.speed_var.get()
            pitch = self.pitch_var.get()
            emotion = self.emotion_var.get()
            
            if voice["provider"] == "piper":
                piper_synthesize(text, voice["id"], output_path, speed=speed, pitch=pitch)
            elif voice["provider"] == "deepgram":
                self.providers["deepgram"].api_key = self.config_manager.get_api_key("deepgram")
                self.providers["deepgram"].synthesize(text, voice["id"], output_path, speed=speed, emotion=emotion)
            elif voice["provider"] == "fish_audio":
                self.providers["fish_audio"].api_key = self.config_manager.get_api_key("fish_audio")
                self.providers["fish_audio"].synthesize(text, voice["id"], output_path, speed=speed, emotion=emotion)
            elif voice["provider"] == "topmedia_ai":
                self.providers["topmedia_ai"].api_key = self.config_manager.get_api_key("topmedia_ai")
                self.providers["topmedia_ai"].synthesize(text, voice["id"], output_path, speed=speed, emotion=emotion)
            
            self.current_output = output_path
            self.config_manager.add_recent_text(text)
            
            self.after(0, self._generation_done, True, f"Saved to: {output_path}")
        except Exception as e:
            self.after(0, self._generation_done, False, str(e))
    
    def _generation_done(self, success, message):
        self.is_generating = False
        self.progress.stop()
        self.progress.grid_remove()
        self.generate_btn.configure(state="normal", text="🎙 Generate Speech")
        
        if success:
            self.status_label.configure(text=message, text_color="#00a8e8")
            self.play_btn.configure(state="normal")
            self.download_btn.configure(state="normal")
            # Auto-play preview
            self.audio_player.play(self.current_output)
            self.play_btn.configure(text="⏸ Pause")
        else:
            self.status_label.configure(text=f"Error: {message}", text_color="red")
            messagebox.showerror("Generation Failed", message)
    
    def download_audio(self):
        if not self.current_output or not os.path.exists(self.current_output):
            return
        
        dest = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3", "*.mp3"), ("WAV", "*.wav"), ("OGG", "*.ogg"), ("All Files", "*.*")],
            initialfile=Path(self.current_output).name
        )
        if dest:
            import shutil
            shutil.copy2(self.current_output, dest)
            self.status_label.configure(text=f"Downloaded to: {dest}", text_color="#00a8e8")
    
    def toggle_favorite(self):
        voice = self.get_selected_voice()
        if not voice:
            return
        self.config_manager.toggle_favorite(voice["id"])
        is_fav = voice["id"] in self.config_manager.get("favorites", [])
        self.fav_btn.configure(text="⭐ Remove Favorite" if is_fav else "⭐ Add to Favorites")
    
    def open_settings(self):
        SettingsWindow(self)

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent: VoiceCraftApp):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings & API Keys")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(self)
        scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        ctk.CTkLabel(scroll, text="API Keys", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        # Deepgram
        ctk.CTkLabel(scroll, text="Deepgram API Key", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.dg_key = ctk.CTkEntry(scroll, show="*", width=400)
        self.dg_key.pack(anchor="w", pady=(0, 10))
        self.dg_key.insert(0, parent.config_manager.get_api_key("deepgram"))
        
        # Fish Audio
        ctk.CTkLabel(scroll, text="Fish Audio API Key", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.fish_key = ctk.CTkEntry(scroll, show="*", width=400)
        self.fish_key.pack(anchor="w", pady=(0, 10))
        self.fish_key.insert(0, parent.config_manager.get_api_key("fish_audio"))
        
        # TopMedia AI
        ctk.CTkLabel(scroll, text="TopMedia AI API Key", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.tm_key = ctk.CTkEntry(scroll, show="*", width=400)
        self.tm_key.pack(anchor="w", pady=(0, 10))
        self.tm_key.insert(0, parent.config_manager.get_api_key("topmedia_ai"))
        
        ctk.CTkLabel(scroll, text="Output Settings", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(20, 10))
        
        ctk.CTkLabel(scroll, text="Output Format", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.format_var = ctk.StringVar(value=parent.config_manager.get("output_format", "mp3"))
        ctk.CTkOptionMenu(scroll, values=["mp3", "wav", "ogg", "flac"], variable=self.format_var).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(scroll, text="Output Directory", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.output_dir = ctk.CTkEntry(scroll, width=400)
        self.output_dir.pack(anchor="w", pady=(0, 10))
        self.output_dir.insert(0, parent.config_manager.get("output_dir"))
        
        ctk.CTkButton(scroll, text="Browse...", command=self.browse_dir).pack(anchor="w")
        
        ctk.CTkButton(scroll, text="Save Settings", font=ctk.CTkFont(size=14, weight="bold"),
                     height=40, command=self.save).pack(anchor="w", pady=(30, 10))
    
    def browse_dir(self):
        dir = filedialog.askdirectory()
        if dir:
            self.output_dir.delete(0, "end")
            self.output_dir.insert(0, dir)
    
    def save(self):
        self.parent.config_manager.set_api_key("deepgram", self.dg_key.get())
        self.parent.config_manager.set_api_key("fish_audio", self.fish_key.get())
        self.parent.config_manager.set_api_key("topmedia_ai", self.tm_key.get())
        self.parent.config_manager.set("output_format", self.format_var.get())
        self.parent.config_manager.set("output_dir", self.output_dir.get())
        
        # Refresh providers
        self.parent.providers["deepgram"] = DeepgramProvider(self.dg_key.get())
        self.parent.providers["fish_audio"] = FishAudioProvider(self.fish_key.get())
        self.parent.providers["topmedia_ai"] = TopMediaProvider(self.tm_key.get())
        
        self.destroy()

if __name__ == "__main__":
    app = VoiceCraftApp()
    app.mainloop()
