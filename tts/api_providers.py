"""API provider integrations for Deepgram, Fish Audio, and TopMedia AI."""
import requests
import json
import os
from typing import Optional

class DeepgramProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepgram.com/v1/speak"
    
    def synthesize(self, text: str, voice_id: str, output_path: str, speed: float = 1.0, emotion: str = "neutral") -> str:
        if not self.api_key:
            raise ValueError("Deepgram API key not set. Go to Settings > API Keys.")
        
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "model": voice_id,
            "speed": speed
        }
        
        url = f"{self.base_url}?model={voice_id}"
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return output_path
        else:
            raise RuntimeError(f"Deepgram API error: {response.status_code} - {response.text}")

class FishAudioProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.fish.audio/v1"
    
    def synthesize(self, text: str, voice_id: str, output_path: str, speed: float = 1.0, emotion: str = "neutral") -> str:
        if not self.api_key:
            raise ValueError("Fish Audio API key not set. Go to Settings > API Keys.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Fish Audio uses a reference_id or model_id
        payload = {
            "text": text,
            "reference_id": voice_id if not voice_id.startswith("fish-") else voice_id,
            "speed": speed
        }
        
        response = requests.post(f"{self.base_url}/tts", headers=headers, json=payload)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            raise RuntimeError(f"Fish Audio API error: {response.status_code} - {response.text}")

class TopMediaProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.topmedia.ai/v1"
    
    def synthesize(self, text: str, voice_id: str, output_path: str, speed: float = 1.0, emotion: str = "neutral") -> str:
        if not self.api_key:
            raise ValueError("TopMedia AI API key not set. Go to Settings > API Keys.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "voice_id": voice_id,
            "speed": speed,
            "emotion": emotion
        }
        
        response = requests.post(f"{self.base_url}/tts", headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            audio_url = data.get("audio_url")
            if audio_url:
                audio_resp = requests.get(audio_url)
                with open(output_path, "wb") as f:
                    f.write(audio_resp.content)
            else:
                with open(output_path, "wb") as f:
                    f.write(response.content)
            return output_path
        else:
            raise RuntimeError(f"TopMedia API error: {response.status_code} - {response.text}")
