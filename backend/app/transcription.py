#app/transcription.py
import whisper
import tempfile

def transcribe_audio(audio_bytes: bytes) -> str:
    model = whisper.load_model("base")
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        result = model.transcribe(tmp.name, fp16=False)
    return result["text"]


'''

# DB setup
Base = declarative_base()

class Transcription(Base):
    __tablename__ = 'transcriptions'
    transcription_id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String)
    file_name = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create DB and session
db_path = "/mnt/data/transcription_db.sqlite3"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Save transcription function
def save_transcription(file_name: str, text: str, file_path: str):
    session = Session()
    transcription = Transcription(
        file_path=file_path,
        file_name=file_name,
        text=text,
        timestamp=datetime.now()
    )
    session.add(transcription)
    session.commit()
    return transcription.transcription_id, transcription.text

# Example call to save dummy transcription
dummy_path = "/mnt/data/example.mp3"
dummy_text = "Dies ist ein Beispiel für eine Transkription."
dummy_id, dummy_saved_text = save_transcription("example.mp3", dummy_text, dummy_path)

import pandas as pd
session = Session()
transcriptions = session.query(Transcription).all()
df = pd.DataFrame([{
    "transcription_id": t.transcription_id,
    "file_name": t.file_name,
    "file_path": t.file_path,
    "text": t.text,
    "timestamp": t.timestamp
} for t in transcriptions])

import ace_tools as tools; tools.display_dataframe_to_user(name="Transkriptionen", dataframe=df)
'''