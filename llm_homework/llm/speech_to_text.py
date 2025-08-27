import sounddevice as sd
import scipy.io.wavfile
import tempfile
from openai import OpenAI

client = OpenAI()

def record_and_transcribe(duration: int = 3) -> str:
    fs = 44100  # Sampling rate
    print("🎙️ Listening... Speak now.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        scipy.io.wavfile.write(tmp.name, fs, audio)
        path = tmp.name

    print("🔁 Transcribing with OpenAI Whisper API...")

    try:
        with open(path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return transcript.text
    except Exception as e:
        return f"❌ Transcription error: {e}"
