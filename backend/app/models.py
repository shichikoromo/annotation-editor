# app/models.py
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = "audio_files"

    audio_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String)
    audio_file = Column(LargeBinary)
    uploaded_at = Column(DateTime, default=datetime.now)

    transcription = relationship("Transcription", back_populates="audio_file")

class Transcription(Base):
    __tablename__ = 'transcriptions'

    transcription_id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(Integer, ForeignKey("audio_files.audio_id", ondelete="CASCADE"))
    file_name = Column(String)
    text = Column(Text)
    transcribed_at = Column(DateTime, default=datetime.now)

    audio_file = relationship("AudioFile", back_populates="transcription")


# DB 接続と初期化
engine = create_engine("sqlite:////db.sqlite3", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
