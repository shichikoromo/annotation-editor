from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from models import AudioFile, Transcript
from db import SessionLocal
from transcription import transcribe_audio

#from app.models import AudioFile, Transcript, RDFAnnotation, AIFAnnotation, Session
#from app.rdf_handler import RDFBuilder
#from app.aif_handler import AIFBuilder

app = FastAPI()

### Hochladen einer Audiodatei ###
@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported.")
    
    content = await file.read()
    session = SessionLocal()
    audio = AudioFile(file_name=file.filename, audio_file=content)

    session.add(audio)
    session.commit()
    session.refresh(audio)
    session.close()

    return {"id": audio.audio_id, "filename": audio.file_name}

### Liste aller hochgeladenen Audiodateien erstellen ###
@app.get("/audiofiles")
def list_audiofiles():
    session = SessionLocal()
    results = session.query(AudioFile).all()
    return [{"id": t.audio_id, "file": t.file_name} for t in results]

### Transkription einer Audiodatei durchführen ###
@app.post("/transcribe/{file_id}")
def transcribe(file_id: int):
    session = SessionLocal()
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

### Liste aller Transkripte erstellen ###
@app.get("/transcripts")
def list_transcripts():
    session = SessionLocal()
    results = session.query(Transcript).all()
    return [{"id": t.transcript_id, "file": t.file_name, "text": t.text} for t in results]
