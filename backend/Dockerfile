FROM python:3.13.3

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ app/
WORKDIR /app/app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

