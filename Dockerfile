#syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app
RUN apt update
RUN apt-get install -y libsndfile1

COPY . /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app/tts-server
ENTRYPOINT ["python"]

CMD ["main.py"]