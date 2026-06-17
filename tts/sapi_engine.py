"""Windows SAPI5 TTS engine using built-in system voices.
Works completely offline with zero downloads. Uses pyttsx3."""
import tempfile
import os
from pathlib import Path
from typing import Optional, List, Dict
import threading

# We import pyttsx3 lazily to avoid import errors on non-Windows platforms
_sapi_engine = None

def _get_engine():
    global _sapi_engine
    if _sapi_engine is None:
        import pyttsx3
        _sapi_engine = pyttsx3.init()
    return _sapi_engine


def get_system_voices() -> List[Dict]:
    """Return all SAPI5 voices installed on this Windows machine."""
    try:
        engine = _get_engine()
        voices = engine.getProperty('voices')
        result = []
        for idx, v in enumerate(voices):
            # Extract gender hint from name/id
            name = v.name
            gender = "neutral"
            name_lower = name.lower()
            if any(x in name_lower for x in ['female', 'woman', 'girl', 'zira', 'hazel', 'cortana', 'anna']):
                gender = "female"
            elif any(x in name_lower for x in ['male', 'man', 'boy', 'david', 'mark', 'james', 'george']):
                gender = "male"
            
            # Language hint from ID (e.g., HKEY_LOCAL_MACHINE...\TTS_MS_EN-US_DAVID_11.0)
            lang = "en"
            if "en-us" in v.id.lower() or "en_us" in v.id.lower():
                lang = "en"
            elif "en-gb" in v.id.lower() or "en_gb" in v.id.lower():
                lang = "en"
            elif "fr-" in v.id.lower() or "fr_" in v.id.lower():
                lang = "fr"
            elif "de-" in v.id.lower() or "de_" in v.id.lower():
                lang = "de"
            elif "es-" in v.id.lower() or "es_" in v.id.lower():
                lang = "es"
            elif "it-" in v.id.lower() or "it_" in v.id.lower():
                lang = "it"
            elif "pt-" in v.id.lower() or "pt_" in v.id.lower():
                lang = "pt"
            elif "ja-" in v.id.lower() or "ja_" in v.id.lower():
                lang = "ja"
            elif "zh-" in v.id.lower() or "zh_" in v.id.lower():
                lang = "zh"
            elif "ru-" in v.id.lower() or "ru_" in v.id.lower():
                lang = "ru"
            elif "ar-" in v.id.lower() or "ar_" in v.id.lower():
                lang = "ar"
            elif "hi-" in v.id.lower() or "hi_" in v.id.lower():
                lang = "hi"
            elif "ko-" in v.id.lower() or "ko_" in v.id.lower():
                lang = "ko"
            
            result.append({
                "id": f"sapi_{idx}",
                "name": name,
                "lang": lang,
                "gender": gender,
                "quality": "medium",
                "provider": "sapi",
                "category": "Built-in Windows Voices",
                "engine_id": idx,
            })
        return result
    except Exception as e:
        print(f"SAPI5 voice detection failed: {e}")
        return []


def synthesize(text: str, voice_idx: int, output_path: str, speed: float = 1.0, pitch: float = 1.0) -> str:
    """Synthesize text using Windows SAPI5 TTS.
    
    pyttsx3 doesn't support direct WAV export easily, so we use a
    background save-to-file approach or the sapi5 COM save-to-wave.
    """
    import pyttsx3
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if 0 <= voice_idx < len(voices):
        engine.setProperty('voice', voices[voice_idx].id)
    
    # Rate adjustment: default is ~200 wpm. Speed 0.5 = 100, 2.0 = 400.
    base_rate = 200
    new_rate = int(base_rate * speed)
    engine.setProperty('rate', max(50, min(500, new_rate)))
    
    # Pitch adjustment is limited in SAPI5 through pyttsx3.
    # We ignore pitch for SAPI since it requires SSXML manipulation.
    
    # pyttsx3 save_to_file is the most reliable cross-platform approach.
    # However, it only works on some backends. On Windows sapi5 we can use
    # the engine's runAndWait() + a temp file approach.
    
    # Actually pyttsx3 supports engine.save_to_file(text, filename) on sapi5.
    temp_wav = output_path
    if not temp_wav.endswith(".wav"):
        temp_wav = temp_wav.rsplit(".", 1)[0] + ".wav"
    
    engine.save_to_file(text, temp_wav)
    engine.runAndWait()
    engine.stop()
    
    # Convert to requested format if not WAV
    if output_path != temp_wav and os.path.exists(temp_wav):
        from pydub import AudioSegment
        AudioSegment.from_wav(temp_wav).export(output_path, format=output_path.split(".")[-1])
        os.remove(temp_wav)
    
    return output_path


def is_available() -> bool:
    """Check if SAPI5/pyttsx3 is available on this system."""
    try:
        import pyttsx3
        pyttsx3.init()
        return True
    except Exception:
        return False
