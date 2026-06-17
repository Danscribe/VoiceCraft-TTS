"""Simple audio playback using pygame mixer."""
import pygame
import os
from pathlib import Path
from pydub import AudioSegment
import tempfile

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._current_path = None
        self._paused = False
    
    def play(self, file_path: str):
        """Play an audio file (any format pydub can read)."""
        if not os.path.exists(file_path):
            return False
        
        # Convert to WAV for pygame playback if needed
        ext = Path(file_path).suffix.lower()
        if ext != ".wav":
            audio = AudioSegment.from_file(file_path)
            fd, wav_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            audio.export(wav_path, format="wav")
            self._current_path = wav_path
        else:
            self._current_path = file_path
        
        pygame.mixer.music.load(self._current_path)
        pygame.mixer.music.play()
        self._paused = False
        return True
    
    def stop(self):
        pygame.mixer.music.stop()
        self._paused = False
    
    def pause(self):
        if pygame.mixer.music.get_busy() and not self._paused:
            pygame.mixer.music.pause()
            self._paused = True
    
    def resume(self):
        if self._paused:
            pygame.mixer.music.unpause()
            self._paused = False
    
    def is_playing(self) -> bool:
        return pygame.mixer.music.get_busy() and not self._paused
    
    def is_paused(self) -> bool:
        return self._paused
