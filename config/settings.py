import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".voicecraft_tts"
CONFIG_FILE = CONFIG_DIR / "config.json"
VOICE_CACHE_FILE = CONFIG_DIR / "voice_cache.json"

DEFAULT_CONFIG = {
    "api_keys": {
        "deepgram": "",
        "fish_audio": "",
        "topmedia_ai": ""
    },
    "default_provider": "piper",
    "default_voice": "en_US-amy-medium",
    "output_format": "mp3",
    "output_dir": str(Path.home() / "Documents" / "VoiceCraft_Audio"),
    "theme": "dark",
    "accent_color": "#00a8e8",
    "recent_texts": [],
    "favorites": [],
    "mood_defaults": {
        "speed": 1.0,
        "pitch": 1.0,
        "emotion": "neutral",
        "stability": 0.5,
        "clarity": 0.7
    }
}

class ConfigManager:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.config = self.load()
    
    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults for new keys
                    merged = DEFAULT_CONFIG.copy()
                    merged.update(loaded)
                    return merged
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()
    
    def get_api_key(self, provider):
        return self.config.get("api_keys", {}).get(provider, "")
    
    def set_api_key(self, provider, key):
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
        self.config["api_keys"][provider] = key
        self.save()
    
    def add_recent_text(self, text, max_items=10):
        recent = self.config.get("recent_texts", [])
        if text in recent:
            recent.remove(text)
        recent.insert(0, text)
        self.config["recent_texts"] = recent[:max_items]
        self.save()
    
    def toggle_favorite(self, voice_id):
        favs = self.config.get("favorites", [])
        if voice_id in favs:
            favs.remove(voice_id)
        else:
            favs.append(voice_id)
        self.config["favorites"] = favs
        self.save()
