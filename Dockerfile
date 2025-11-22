FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget gnupg apt-transport-https ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps firefox

COPY . .

CMD ["python", "main.py"]
