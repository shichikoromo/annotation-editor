from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import Transcript, AIFAnnotation, RDFAnnotation
from db import SessionLocal
from schemas import AIFAnnotationInput
from aif_handler import AIFBuilder
import os

app = FastAPI()

### AIF-Annotation speichern / aktualisieren ###
@app.post("/annotate_aif/{file_id}")
def annotate_aif(file_id: int, payload: AIFAnnotationInput):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=file_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    rdf_ann = session.query(RDFAnnotation).filter_by(transcript_id=file_id,sentence_id=payload.sentence_id).first()
    if not rdf_ann:
        session.close()
        raise HTTPException(status_code=404, detail="RDF-Annotation not found")

    aif_ann = session.query(AIFAnnotation).filter_by(aif_id=f"{file_id}_{payload.sentence_id}").first()

    if aif_ann:
        # Update
        aif_ann.type = payload.type
        aif_ann.supports = payload.supports
    else:
        # Create
        aif_ann = AIFAnnotation(
            aif_id=f"{file_id}_{payload.sentence_id}",
            transcript_id=file_id,
            rdf_id=rdf_ann.rdf_id,
            sentence_id =payload.sentence_id,
            type=payload.type,
            supports=payload.supports
        )
        session.add(aif_ann)
    
    session.commit()
    session.refresh(aif_ann)
    session.close()

    return JSONResponse(content=jsonable_encoder(aif_ann))

### AIF-Annotationen für ein bestimmtes Transkript abrufen ###
@app.get("/aif_annotation/{transcript_id}")
def get_aif_annotations(transcript_id: int):
    session = SessionLocal()
    annotations = session.query(AIFAnnotation).filter_by(transcript_id=transcript_id).all()
    session.close()
    return [ann.__dict__ for ann in annotations]

### AIF-Annotationen als XML exportieren ###
@app.get("/export_aif/{transcript_id}")
def export_aif(transcript_id: int):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=transcript_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    aif_annotations = session.query(AIFAnnotation).join(Transcript).filter(
        AIFAnnotation.transcript_id == transcript_id
    ).all()

    if not aif_annotations:
        session.close()
        raise HTTPException(status_code=404, detail="AIF-Annotationen not found")

    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower()

    builder = AIFBuilder(namespace)
    builder.build_aif(aif_annotations)
    aif_xml = builder.serialize()

    session.close()

    return JSONResponse(content={"aif_xml": aif_xml})
