from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Transcript(Base):
    __tablename__ = "transcripts"

    transcript_id = Column(Integer, primary_key=True)
    file_name = Column(String)
    text = Column(Text)
    transcribed_at = Column(DateTime)

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

class RDFDocument(Base):
    __tablename__ = "rdf_documents"

    rdf_doc_id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    rdf_xml = Column(Text)
    rdf_doc_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="rdf_document")
