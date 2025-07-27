#app/transcription.py
import whisper
import tempfile

def transcribe_audio(audio_bytes: bytes) -> str:
    model = whisper.load_model("small")
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        result = model.transcribe(tmp.name, fp16=False)
    return result["text"]
