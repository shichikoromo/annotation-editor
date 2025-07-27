# app/models.py
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class AudioFile(Base):
    __tablename__ = "audio_files"

    audio_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String)
    audio_file = Column(LargeBinary)
    uploaded_at = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="audio_file")

class Transcript(Base):
    __tablename__ = 'transcripts'

    transcript_id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(Integer, ForeignKey("audio_files.audio_id", ondelete="CASCADE"))
    file_name = Column(String)
    text = Column(Text)
    transcribed_at = Column(DateTime, default=datetime.now)

    audio_file = relationship("AudioFile", back_populates="transcript")
    rdf_annotation = relationship("RDFAnnotation", back_populates="transcript")
    rdf_document = relationship("RDFDocument", back_populates="transcript")

class RDFAnnotation(Base):
    __tablename__ = "rdf_annotations"

    rdf_id = Column(String(64000), primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    sentence_id = Column(Integer)
    sentence = Column(Text)
    subject = Column(Text)
    predicate = Column(Text) 
    object_ = Column(Text)  
    rdf_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="rdf_annotation")
    aif_annotation = relationship("AIFAnnotation", back_populates="rdf_annotation")

class RDFDocument(Base):
    __tablename__ = "rdf_documents"

    rdf_doc_id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    rdf_xml = Column(Text) 
    rdf_doc_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="rdf_document")

class AIFAnnotation(Base):
    __tablename__ = "aif_annotations"

    aif_id = Column(String(64000), primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    rdf_id = Column(Integer, ForeignKey("rdf_annotations.rdf_id"))
    sentence_id = Column(Integer)
    type = Column(Text)
    supports = Column(Text) 
    aif_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="aif_annotation")
    rdf_annotation = relationship("RDFAnnotation", back_populates="aif_annotation")

class AIFDocument(Base):
    __tablename__ = "aif_documents"

    aif_doc_id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    aif_xml = Column(Text) 
    aif_doc_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="aif_document")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")

# DB 接続と初期化
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
#engine = create_engine("sqlite:////backend/db.sqlite3", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)