from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import Transcript, AIFArgument, RDFAnnotation
from db import SessionLocal
from schemas import AIFArgumentInput
from aif_handler import AIFBuilder
from sqlalchemy.orm import aliased
import os, datetime

app = FastAPI()

### AIF-Argumente speichern / aktualisieren ###
@app.post("/add_aif/{file_id}")
def add_aif(file_id: int, payload: AIFArgumentInput):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=file_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    # Source/Target Annotation holen
    source_ann = session.query(RDFAnnotation).filter_by(transcript_id=file_id, sentence_id=payload.source_id).first()
    target_ann = session.query(RDFAnnotation).filter_by(transcript_id=file_id, sentence_id=payload.target_id).first()

    if not source_ann or not target_ann:
        session.close()
        raise HTTPException(status_code=404, detail="Source or target RDF-Annotation not found")

    # aif_id eindeutig konstruieren
    aif_id = f"{file_id}_{payload.source_id}"

    aif_arg = session.query(AIFArgument).filter_by(aif_id=aif_id).first()

    if aif_arg:
        # Update
        aif_arg.i_source_id = source_ann.rdf_id
        aif_arg.i_target_id = target_ann.rdf_id
        aif_arg.s_relation = payload.relation
        aif_arg.aif_timestamp = datetime.datetime.now()
    else:
        # Create
        aif_arg = AIFArgument(
            aif_id=aif_id,
            transcript_id=file_id,
            i_source_id=source_ann.rdf_id,
            i_target_id=target_ann.rdf_id,
            s_relation=payload.relation,
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
    arguments = session.query(AIFArgument).filter_by(transcript_id=transcript_id).all()
    session.close()
    return [arg.__dict__ for arg in arguments]

### AIF-Argumente als XML exportieren ###
@app.get("/export_aif/{transcript_id}")
def export_aif(transcript_id: int):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=transcript_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    #aif_arguments = session.query(AIFArgument).join(Transcript).filter(AIFArgument.transcript_id == transcript_id).all()

    source_ann = aliased(RDFAnnotation)
    target_ann = aliased(RDFAnnotation)

    aif_arguments = session.query(AIFArgument).\
        join(source_ann, AIFArgument.i_source_id == source_ann.rdf_id).\
        join(target_ann, AIFArgument.i_target_id == target_ann.rdf_id).\
        filter(AIFArgument.transcript_id == transcript_id).all()

    if not aif_arguments:
        session.close()
        raise HTTPException(status_code=404, detail="AIF-Argument not found")

    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower()

    builder = AIFBuilder(namespace)
    builder.build_aif(aif_arguments)
    aif_xml = builder.serialize()

    session.close()

    return JSONResponse(content={"aif_xml": aif_xml})
