from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = "audio_files"

    audio_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    audio_file = Column(LargeBinary)
    uploaded_at = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="audio_file")

class Transcript(Base):
    __tablename__ = "transcripts"

    transcript_id = Column(Integer, primary_key=True)
    audio_id = Column(Integer, ForeignKey("audio_files.audio_id", ondelete="CASCADE"))
    file_name = Column(String)
    text = Column(Text)
    transcribed_at = Column(DateTime, default=datetime.now)

    audio_file = relationship("AudioFile", back_populates="transcript")