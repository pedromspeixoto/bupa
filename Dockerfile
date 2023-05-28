#syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app
RUN apt update
RUN apt-get install -y libsndfile1 ffmpeg cmake git

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

# install gpt4all
WORKDIR /app/tts-server/
RUN git clone --recurse-submodules https://github.com/nomic-ai/gpt4all
WORKDIR gpt4all/gpt4all-backend/
RUN mkdir build
WORKDIR build
RUN cmake ..
RUN cmake --build . --parallel

# setup gpt4all python package
WORKDIR ../../gpt4all-bindings/python
RUN pip3 install -e .

EXPOSE 5000
WORKDIR /app/tts-server
ENTRYPOINT ["python"]

ENV TRAINER_TELEMETRY=0

CMD ["main.py"]