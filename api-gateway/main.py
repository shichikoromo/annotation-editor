from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

TRANSCRIPTION_URL = "http://transcription-service:8001"
RDF_URL = "http://rdf-annotation-service:8002"
AIF_URL = "http://aif-argument-service:8003"

### Audio-Datei hochladen ###
@app.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported.")
    
    content = await file.read()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TRANSCRIPTION_URL}/upload_audio/",
            files={"file": (file.filename, content, file.content_type)},
        )
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/audiofiles")
async def list_audiofiles():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRANSCRIPTION_URL}/audiofiles")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### Transkription starten ###
@app.post("/transcribe/{file_id}")
async def transcribe(file_id: int):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(f"{TRANSCRIPTION_URL}/transcribe/{file_id}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### Transkript-Liste anzeigen ###
@app.get("/transcripts")
async def list_transcripts():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRANSCRIPTION_URL}/transcripts")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### RDF-Annotation absenden ###
@app.post("/annotate_rdf/{file_id}")
async def annotate_rdf(file_id: int, payload: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{RDF_URL}/annotate_rdf/{file_id}", json=payload)
    return JSONResponse(content=response.json(), status_code=response.status_code)

### RDF-Annotationen abrufen ###
@app.get("/rdf_annotation/{transcript_id}")
async def get_rdf_annotations(transcript_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RDF_URL}/rdf_annotation/{transcript_id}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### RDF als XML exportieren ###
@app.get("/export_rdf/{transcript_id}")
async def export_rdf(transcript_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RDF_URL}/export_rdf/{transcript_id}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### AIF-Argument absenden ###
@app.post("/add_aif/{file_id}")
async def add_aif(file_id: int, payload: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AIF_URL}/add_aif/{file_id}", json=payload)
    return JSONResponse(content=response.json(), status_code=response.status_code)

### AIF-Argument abrufen ###
@app.get("/aif_argument/{transcript_id}")
async def get_aif_arguments(transcript_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AIF_URL}/aif_argument/{transcript_id}")
    return JSONResponse(content=response.json(), status_code=response.status_code)

### AIF als XML exportieren ###
@app.get("/export_aif/{transcript_id}")
async def export_aif(transcript_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AIF_URL}/export_aif/{transcript_id}")
    return JSONResponse(content=response.json(), status_code=response.status_code)
