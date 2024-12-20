FROM python:3.12.7-slim

WORKDIR /app



RUN apt-get update && apt-get install -y \  
    libasound2 \
    espeak \
    pip install uv && \

