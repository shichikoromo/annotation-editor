# Aussagen- und Argumentannotationseditor

Ein interaktives Tool zur Transkription und Annotation von historischen Audiointerviews.

Dieses Projekt wurde im Rahmen der Veranstaltung "63490 Projektpraktikum Data Science für Digital Humanities" entwickelt.

## Architektur

Die Anwendung ist als Microservice-System mit folgenden Komponenten aufgebaut:

- **Backend (FastAPI)**: API für Transkription, RDF- und AIF-Annotation
- **Frontend (Jupyter Notebook + ipywidgets)**: Interaktive Benutzeroberfläche
- **Datenbank (SQLite)**: Speicherung der Transkripte und Annotationen
- **Docker**: Containerisierung aller Komponenten


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
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── transcription.py
│   │   ├── rdf\_handler.py
│   │   ├── aif\_handler.py
│   │   ├── db.sqlite3
│   └── Dockerfile
├── frontend/
│   ├── editor.ipynb
│   ├── uploads/
│   ├── out/
│   └── Dockerfile
└── docker-compose.yml
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

* Öffnen Sie [http://localhost:8777](http://localhost:8777) im Browser.
* Notebook: `frontend/editor_notebook.ipynb`

### Funktionen im Notebook

* MP3-Datei hochladen
* Transkription ausführen
* Aussage-Annotation (RDF) hinzufügen
* Argument-Annotation (AIF) strukturieren
* RDF/AIF als XML exportieren
