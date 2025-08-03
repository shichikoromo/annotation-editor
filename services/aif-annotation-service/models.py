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

    rdf_annotations = relationship("RDFAnnotation", back_populates="transcript")
    aif_annotations = relationship("AIFAnnotation", back_populates="transcript")
    aif_document = relationship("AIFDocument", back_populates="transcript")


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

    transcript = relationship("Transcript", back_populates="rdf_annotations")
    aif_annotations = relationship("AIFAnnotation", back_populates="rdf_annotation")


class AIFAnnotation(Base):
    __tablename__ = "aif_annotations"

    aif_id = Column(String(64000), primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    rdf_id = Column(String(64000), ForeignKey("rdf_annotations.rdf_id"))
    sentence_id = Column(Integer)
    type = Column(Text)
    supports = Column(Text)
    aif_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="aif_annotations")
    rdf_annotation = relationship("RDFAnnotation", back_populates="aif_annotations")


class AIFDocument(Base):
    __tablename__ = "aif_documents"

    aif_doc_id = Column(Integer, primary_key=True, index=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    aif_xml = Column(Text)
    aif_doc_timestamp = Column(DateTime, default=datetime.now)

    transcript = relationship("Transcript", back_populates="aif_document")
