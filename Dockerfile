FROM python:3.11-slim

RUN apt update && apt install -y ffmpeg

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app

EXPOSE 5000
CMD ["python", "app/app.py"]