#app/transcription.py
import whisper
import tempfile
import datetime

model = whisper.load_model("small")

def transcribe_audio(audio_bytes: bytes) -> str:
    print(datetime.datetime.now(), "transcription.py: transcribe_audio()")
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        print(datetime.datetime.now(), "transcription.py: tmp.write(audio_bytes)")
        tmp.flush()
        result = model.transcribe(tmp.name, fp16=False)
        print(datetime.datetime.now(), "transcription.py: result:", result)
    return result["text"]
