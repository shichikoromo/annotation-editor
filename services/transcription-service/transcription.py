# transcription.py
import whisper
import tempfile
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = whisper.load_model("base")

def transcribe_audio(audio_bytes: bytes) -> str:
    logger.info(f"{datetime.now()} Starting transcription")
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            result = model.transcribe(tmp.name, fp16=False)
            logger.info(f"{datetime.now()} Transcription result: {result['text'][:50]}...")
        return result["text"]
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return ""
