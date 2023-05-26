#syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app
RUN apt update
RUN apt-get install -y libsndfile1 ffmpeg

COPY . /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app/tts-server
ENTRYPOINT ["python"]

ENV TRAINER_TELEMETRY=0

CMD ["main.py"]