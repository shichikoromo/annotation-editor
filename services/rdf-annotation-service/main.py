from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import RDFAnnotation, Transcript
from db import SessionLocal
from schemas import RDFAnnotationInput
from rdf_handler import RDFBuilder
import os

app = FastAPI()

### RDF-Annotation speichern / aktualisieren ###
@app.post("/annotate_rdf/{file_id}")
def annotate_rdf(file_id: int, payload: RDFAnnotationInput):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=file_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    rdf_ann = session.query(RDFAnnotation).filter_by(rdf_id=f"{file_id}_{payload.sentence_id}").first()

    if rdf_ann:
        # Update
        rdf_ann.subject = payload.subject
        rdf_ann.predicate = payload.predicate
        rdf_ann.object_ = payload.object_
    else:
        # Create
        rdf_ann = RDFAnnotation(
            rdf_id=f"{file_id}_{payload.sentence_id}",
            transcript_id=file_id,
            sentence_id =payload.sentence_id,
            sentence=payload.sentence,
            subject=payload.subject,
            predicate=payload.predicate,
            object_=payload.object_
        )
        session.add(rdf_ann)
    
    session.commit()
    session.refresh(rdf_ann)
    session.close()

    print(jsonable_encoder(rdf_ann))

    return JSONResponse(content=jsonable_encoder(rdf_ann))

### RDF-Annotationen für ein bestimmtes Transkript abrufen ###
@app.get("/rdf_annotation/{transcript_id}")
def get_rdf_annotations(transcript_id: int):
    session = SessionLocal()
    annotations = session.query(RDFAnnotation).filter_by(transcript_id=transcript_id).all()
    session.close()
    return [ann.__dict__ for ann in annotations]

### RDF-Annotationen als XML exportieren ###
@app.get("/export_rdf/{transcript_id}")
def export_rdf(transcript_id: int):
    session = SessionLocal()

    transcript = session.query(Transcript).filter_by(transcript_id=transcript_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    annotations = session.query(RDFAnnotation).filter(RDFAnnotation.transcript_id == transcript_id).order_by(RDFAnnotation.sentence_id).all()

    if not annotations:
        raise HTTPException(status_code=404, detail="RDF-Annotation not found")
     
    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower()

    builder = RDFBuilder(namespace)
    annot =  sorted(annotations, key=lambda d: d.sentence_id, reverse=True)
    builder.build_rdf(annot)

    rdf_xml = builder.serialize()

    return JSONResponse(content={"rdf_xml": rdf_xml})