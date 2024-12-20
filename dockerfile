FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y libportaudio2 espeak \
    && pip install uv \
    && uv pip install --system -r requirements.txt

COPY . .

CMD ["uv", "run", "python", "main.py"]