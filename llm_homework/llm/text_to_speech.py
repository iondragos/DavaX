from gtts import gTTS
import os
import pygame
import uuid

AUDIO_DIR = "audio"

def speak_text(text: str, play: bool = True, filename: str = None):
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    filename = filename or f"tts_{uuid.uuid4().hex}.mp3"
    path = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang="en")
    tts.save(path)

    if play:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

