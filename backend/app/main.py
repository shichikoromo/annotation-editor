#app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models import AudioFile, Transcript, RDFAnnotation, AIFAnnotation, Session
from app.transcription import transcribe_audio
from app.rdf_handler import RDFBuilder
from app.aif_handler import AIFBuilder
from app.schemas import RDFAnnotationInput, AIFAnnotationInput
import os

app = FastAPI()

@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported.")
    
    content = await file.read()
    session = Session()
    audio = AudioFile(file_name=file.filename, audio_file=content)

    session.add(audio)
    session.commit()
    print(f"Gespeichert mit ID: {audio.audio_id}")
    session.refresh(audio)
    session.close()

    return {"id": audio.audio_id, "filename": audio.file_name}

@app.get("/audiofiles")
def list_audiofiles():
    session = Session()
    results = session.query(AudioFile).all()
    return [{"id": t.audio_id, "file": t.file_name} for t in results]

@app.post("/transcribe/{file_id}")
def transcribe(file_id: int):
    session = Session()
    audio = session.query(AudioFile).filter(AudioFile.audio_id == file_id).first()
    
    if not audio:
        raise HTTPException(status_code=404, detail="File not found")

    response = transcribe_audio(audio.audio_file)

    transcript = Transcript(audio_id=audio.audio_id, file_name=audio.file_name, text=response)

    session.add(transcript)
    session.commit()
    session.refresh(transcript)
    session.close()

    return JSONResponse(content={"response": response})

@app.get("/transcripts")
def list_transcripts():
    session = Session()
    results = session.query(Transcript).all()
    return [{"id": t.transcript_id, "file": t.file_name, "text": t.text} for t in results]

@app.post("/annotate_rdf/{file_id}")
def annotate_rdf(file_id: int, payload: RDFAnnotationInput):
    session = Session()

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
    
    #session.add(rdf_ann)
    session.commit()
    session.refresh(rdf_ann)
    session.close()

    print(jsonable_encoder(rdf_ann))

    return JSONResponse(content=jsonable_encoder(rdf_ann))

@app.get("/rdf_annotation/{transcript_id}")
def get_rdf_annotations(transcript_id: int):
    session = Session()
    annotations = session.query(RDFAnnotation).filter_by(transcript_id=transcript_id).all()
    session.close()
    return [ann.__dict__ for ann in annotations]


@app.get("/export_rdf/{transcript_id}")
def export_rdf(transcript_id: int):
    session = Session()

    transcript = session.query(Transcript).filter_by(transcript_id=transcript_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    annotations = session.query(RDFAnnotation).filter(RDFAnnotation.transcript_id == transcript_id).order_by(RDFAnnotation.sentence_id).all()

    if not annotations:
        raise HTTPException(status_code=404, detail="RDF-Annotationen not found")
     
    # ファイル名から namespace を生成
    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower()

    builder = RDFBuilder(namespace)

    annot =  sorted(annotations, key=lambda d: d.sentence_id, reverse=True)
    builder.build_rdf(annot)

    rdf_xml = builder.serialize()

    return JSONResponse(content={"rdf_xml": rdf_xml})


@app.post("/annotate_aif/{file_id}")
def annotate_aif(file_id: int, payload: AIFAnnotationInput):
    session = Session()

    transcript = session.query(Transcript).filter_by(transcript_id=file_id).first()
    if not transcript:
        session.close()
        raise HTTPException(status_code=404, detail="Transcript not found")

    rdf_ann = session.query(RDFAnnotation).filter_by(transcript_id=file_id,sentence_id=payload.sentence_id).first()
    if not rdf_ann:
        session.close()
        raise HTTPException(status_code=404, detail="RDF Annotation not found")

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
            sentence_id =payload.sentence_id,
            type=payload.type,
            supports=payload.supports
        )
        session.add(aif_ann)
    
    session.commit()
    session.refresh(aif_ann)
    session.close()

    print(jsonable_encoder(aif_ann))

    return JSONResponse(content=jsonable_encoder(aif_ann))

@app.get("/export_aif/{transcript_id}")
def export_aif(transcript_id: int):
    session = Session()

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

    # ファイル名から namespace を生成
    namespace = os.path.splitext(os.path.basename(transcript.file_name))[0].lower() + "/"

    builder = AIFBuilder(namespace)

    annotations_data = []
    for ann in aif_annotations:
        annotations_data.append({
            "rdf_id": ann.rdf_id,             
            "role": ann.role,                  
            "supports": ann.supports or None   
        })

    builder.build_aif(annotations_data)

    aif_xml = builder.serialize()

    session.close()
    return JSONResponse(content={"aif_xml": aif_xml})
