"""Offline Piper TTS engine with voice downloading."""
import os
import json
import urllib.request
import shutil
import sys
from pathlib import Path
from typing import Optional
import numpy as np
import soundfile as sf
import subprocess

PIPER_DIR = Path.home() / ".voicecraft_tts" / "piper_voices"
PIPER_DIR.mkdir(parents=True, exist_ok=True)

# HuggingFace base URL for Piper voices
HF_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0"


def _get_bundle_dir() -> Optional[Path]:
    """Return the bundled voices directory when running as a PyInstaller .exe."""
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts to _MEIPASS
        bundle = Path(sys._MEIPASS) / "piper_voices"
        if bundle.exists():
            return bundle
    return None


def _install_bundled_voice(voice_id: str) -> bool:
    """Copy a bundled voice from the installer to user cache."""
    bundle = _get_bundle_dir()
    if not bundle:
        return False
    model_src = bundle / f"{voice_id}.onnx"
    config_src = bundle / f"{voice_id}.onnx.json"
    if not model_src.exists() or not config_src.exists():
        return False
    
    model_dst = PIPER_DIR / f"{voice_id}.onnx"
    config_dst = PIPER_DIR / f"{voice_id}.onnx.json"
    
    try:
        shutil.copy2(str(model_src), str(model_dst))
        shutil.copy2(str(config_src), str(config_dst))
        return True
    except Exception:
        return False


def get_voice_path(voice_id: str) -> Optional[Path]:
    """Check if a voice model is already downloaded (or bundled)."""
    model_path = PIPER_DIR / f"{voice_id}.onnx"
    config_path = PIPER_DIR / f"{voice_id}.onnx.json"
    if model_path.exists() and config_path.exists():
        return model_path
    
    # Try installing from bundled voices (offline installer)
    if _install_bundled_voice(voice_id):
        if model_path.exists() and config_path.exists():
            return model_path
    return None

def download_voice(voice_id: str, progress_callback=None) -> Optional[Path]:
    """Download a Piper voice from HuggingFace."""
    parts = voice_id.split("-")
    if len(parts) < 2:
        return None
    
    lang = parts[0]
    quality = "medium"
    if "-low" in voice_id:
        quality = "low"
    elif "-high" in voice_id:
        quality = "high"
    elif "-x_low" in voice_id:
        quality = "x_low"
    
    # Construct URL path
    voice_name = voice_id.replace(f"{lang}-", "").replace(f"-{quality}", "")
    url_base = f"{HF_BASE}/{lang}/{voice_name}/{quality}"
    
    model_name = f"{voice_id}.onnx"
    config_name = f"{voice_id}.onnx.json"
    
    model_path = PIPER_DIR / model_name
    config_path = PIPER_DIR / config_name
    
    try:
        if not model_path.exists():
            if progress_callback:
                progress_callback(0.1, f"Downloading {voice_id} model...")
            urllib.request.urlretrieve(f"{url_base}/{model_name}", model_path)
        
        if not config_path.exists():
            if progress_callback:
                progress_callback(0.5, f"Downloading {voice_id} config...")
            urllib.request.urlretrieve(f"{url_base}/{config_name}", config_path)
        
        if progress_callback:
            progress_callback(1.0, "Done")
        return model_path
    except Exception as e:
        print(f"Failed to download voice {voice_id}: {e}")
        # Cleanup partial files
        if model_path.exists():
            model_path.unlink()
        if config_path.exists():
            config_path.unlink()
        return None

def synthesize(text: str, voice_id: str, output_path: str, speed: float = 1.0, pitch: float = 1.0):
    """Synthesize text using Piper TTS."""
    model_path = get_voice_path(voice_id)
    if not model_path:
        model_path = download_voice(voice_id)
    if not model_path:
        raise RuntimeError(f"Voice {voice_id} not available and could not be downloaded.")
    
    # Use piper-tts command if available, else fallback to a simple implementation
    # For robustness, we'll write a WAV then optionally process speed/pitch
    wav_path = output_path
    if not wav_path.endswith(".wav"):
        wav_path = wav_path.rsplit(".", 1)[0] + ".wav"
    
    try:
        # Try using piper command-line
        cmd = [
            "piper",
            "--model", str(model_path),
            "--output_file", wav_path
        ]
        subprocess.run(cmd, input=text.encode("utf-8"), check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Fallback: try python module import if available
        try:
            from piper import PiperVoice
            voice = PiperVoice.load(str(model_path))
            with sf.SoundFile(wav_path, mode="w", samplerate=voice.config.sample_rate, channels=1, format="WAV") as f:
                for audio_bytes in voice.synthesize_stream_raw(text):
                    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
                    f.write(audio_array)
        except Exception as e2:
            raise RuntimeError(f"Piper synthesis failed: {e2}")
    
    # Apply speed/pitch modification via pydub if needed
    if abs(speed - 1.0) > 0.05 or abs(pitch - 1.0) > 0.05:
        from pydub import AudioSegment
        audio = AudioSegment.from_wav(wav_path)
        if abs(speed - 1.0) > 0.05:
            # Change speed by altering frame rate and resampling
            new_rate = int(audio.frame_rate * (1.0 / speed))
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_rate})
            audio = audio.set_frame_rate(audio.frame_rate)
        if abs(pitch - 1.0) > 0.05:
            semitones = (pitch - 1.0) * 12  # rough mapping
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * (2 ** (semitones / 12.0)))
            })
            audio = audio.set_frame_rate(audio.frame_rate)
        audio.export(wav_path, format="wav")
    
    if output_path != wav_path:
        from pydub import AudioSegment
        AudioSegment.from_wav(wav_path).export(output_path, format=output_path.split(".")[-1])
    
    return output_path
