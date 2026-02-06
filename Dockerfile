FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["uvicorn", "presentation_agent.server:app", "--host", "0.0.0.0", "--port", "10000"]
