FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -U pip \
 && python -m pip install --no-cache-dir -r requirements.txt


COPY tts/ /app/

ENV TTS_VOICES_DIR=/app/tts_api/voices

EXPOSE 8000 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
