# Aussagen- und Argumentannotationseditor

Ein interaktives Tool zur Transkription und Annotation von historischen Audiointerviews.

Dieses Projekt wurde im Rahmen der Veranstaltung "63490 Projektpraktikum Data Science für Digital Humanities" entwickelt.

## Architektur

Die Anwendung ist als Microservice-System mit folgenden Komponenten aufgebaut:

- **API Gateway**: API für Transkription, RDF- und AIF-Annotation
- **Services**
  - **Transkription**
  - **RDF-Annotation-Service**
  - **AIF-Annotation-Service**
- **Frontend (Jupyter Notebook)**: Interaktive Benutzeroberfläche
- **Datenbank (PostgeSQL)**: Speicherung der Transkripte und Annotationen
- **Docker**: Containerisierung der Komponenten

## Technologien

* Python 3.10
* ipywidgets
* FastAPI
* SQLite + SQLAlchemy
* Whisper
* rdflib
* Docker


## Ordnerstruktur
```
annotationeditor/
├── docker-compose.yml
│
├── api-gateway/               
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                 
│   ├── editor.ipynb
│   ├── uploads/
│   ├── out/
│   ├── requirements.txt
│   └── Dockerfile
│
├── services/
│   ├── transcription-service/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── trenscription.py
│   │   ├── db.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── rdf-annotation-service/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── rdf_handler.py
│   │   ├── db.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── aif-annotation-service/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── aif_handler.py
│       ├── db.py
│       ├── requirements.txt
│       └── Dockerfile
│
├── db/

```

## Anwendung

### 1. Projekt clonen

```bash
git clone https://github.com/shichikoromo/annotation-editor.git
```

### 2. Projekt starten

```bash
docker-compose up --build
```

### 3. Zugriff auf Jupyter Notebook

* Öffnen Sie [http://localhost:7777](http://localhost:7777) im Browser.
* Notebook: `editor.ipynb`

### Funktionen im Notebook

* MP3-Datei hochladen
* Transkription ausführen
* Aussage-Annotation (RDF) hinzufügen
* Argument-Annotation (AIF) strukturieren
* RDF/AIF als XML exportieren
