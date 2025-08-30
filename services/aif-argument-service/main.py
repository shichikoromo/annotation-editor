from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import Transcript, AIFArgument, RDFAnnotation
from db import SessionLocal
from schemas import AIFArgumentInput
from aif_handler import AIFBuilder
import os

app = FastAPI()

### AIF-Argumente speichern / aktualisieren ###
@app.post("/add_aif/{file_id}")
def add_aif(file_id: int, payload: AIFArgumentInput):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=file_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    rdf_ann = session.query(RDFAnnotation).filter_by(transcript_id=file_id,sentence_id=payload.sentence_id).first()
    if not rdf_ann:
        session.close()
        raise HTTPException(status_code=404, detail="RDF-Annotation not found")

    aif_arg = session.query(AIFArgument).filter_by(aif_id=f"{file_id}_{payload.sentence_id}").first()

    if aif_arg:
        # Update
        aif_arg.type = payload.type
        aif_arg.supports = payload.supports
    else:
        # Create
        aif_arg = AIFArgument(
            aif_id=f"{file_id}_{payload.sentence_id}",
            transcript_id=file_id,
            rdf_id=rdf_ann.rdf_id,
            sentence_id =payload.sentence_id,
            type=payload.type,
            supports=payload.supports
        )
        session.add(aif_arg)
    
    session.commit()
    session.refresh(aif_arg)
    session.close()

    return JSONResponse(content=jsonable_encoder(aif_arg))

### AIF-Argumente für ein bestimmtes Transkript abrufen ###
@app.get("/aif_argument/{transcript_id}")
def get_aif_arguments(transcript_id: int):
    session = SessionLocal()
    annotations = session.query(AIFArgument).filter_by(transcript_id=transcript_id).all()
    session.close()
    return [ann.__dict__ for ann in annotations]

### AIF-Argumente als XML exportieren ###
@app.get("/export_aif/{transcript_id}")
def export_aif(transcript_id: int):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=transcript_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    aif_arguments = session.query(AIFArgument).join(Transcript).filter(
        AIFArgument.transcript_id == transcript_id
    ).all()

    if not aif_arguments:
        session.close()
        raise HTTPException(status_code=404, detail="AIF-Argument not found")

    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower()

    builder = AIFBuilder(namespace)
    builder.build_aif(aif_arguments)
    aif_xml = builder.serialize()

    session.close()

    return JSONResponse(content={"aif_xml": aif_xml})
