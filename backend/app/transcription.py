#app/transcription.py
import whisper
import tempfile
import datetime

print(datetime.datetime.now(), "transcription.py: load_model(\"base\")")
model = whisper.load_model("small")
print(datetime.datetime.now(), "transcription.py: load_model(\"base\")")

def transcribe_audio(audio_bytes: bytes) -> str:
    print(datetime.datetime.now(), "transcription.py: transcribe_audio()")
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        print(datetime.datetime.now(), "transcription.py: tmp.write(audio_bytes)")
        tmp.flush()
        result = model.transcribe(tmp.name, fp16=False)
        print(datetime.datetime.now(), "transcription.py: result:", result)
    return result["text"]
