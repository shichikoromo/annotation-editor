FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .

RUN apt-get clean && apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

# Whisper Model
RUN python -c "import whisper; whisper.load_model('base')"

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
