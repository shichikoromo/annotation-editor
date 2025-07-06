#app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.models import AudioFile, Transcription, Session
from app.transcription import transcribe_audio

app = FastAPI()

#engine = create_engine("sqlite:////db.sqlite3")
#Base.metadata.create_all(engine)
#Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#session = SessionLocal()
#Session = sessionmaker(bind=engine)

@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported.")
    
    content = await file.read()
    session = Session()
    audio = AudioFile(file_name=file.filename, audio_file=content)

    session.add(audio)
    session.commit()
    session.refresh(audio)
    session.close()

    return {"id": audio.audio_id, "filename": audio.file_name}

@app.post("/transcribe/{file_id}")
def transcribe(file_id: int):
    session = Session()
    audio = session.query(AudioFile).filter(AudioFile.audio_id == file_id).first()
    
    if not audio:
        raise HTTPException(status_code=404, detail="File not found")

    response = transcribe_audio(audio.audio_file)

    transcript = Transcription(audio_id=audio.audio_id, file_name=audio.file_name, text=response)

    session.add(transcript)
    session.commit()
    session.refresh(transcript)
    session.close()

    return JSONResponse(content={"response": response})

@app.get("/transcriptions/")
def list_transcriptions():
    session = Session()
    results = session.query(Transcription).all()
    return [{"id": t.transcription_id, "text": t.text, "file": t.file_name} for t in results]
