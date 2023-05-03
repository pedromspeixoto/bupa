# openai-tts-server

This repo contains the code for an example of a text to speech server that uses the OpenAI API to fetch
customised answers to questions based on a given context.

## Showcase

https://user-images.githubusercontent.com/35801678/235898200-560442c3-7408-4bfa-a239-d141a72e5605.mp4


## Prerequisites

- Python 3.9

## Installation

1. Clone the repo
2. Install the dependencies with `pip install -r requirements.txt`
3. Create a `tts-server/.env` file with the following variables:

```bash
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_MODEL=gpt-3.5-turbo
```

## Usage

### Using the CLI

1. Run the server with `python tts-server/main.py`
2. Access the server running at `http://localhost:8080/`, configure the Bopa bot and submit a question 
3. Or, as an alternative, send a POST request to `http://localhost:8080/ask` with the following JSON body:

```json
{
    "mood": "happy",
    "persona": "yoda",
    "text": "What is human life expectancy in the United States?"
}
```

### Using Docker

1. Build the Docker image with `docker build -t bupa-bot .`
2. Run the Docker container with `docker run -p 5001:8080 bupa-bot`
3. Access the server running at `http://localhost:5001/`, configure the Bopa bot and submit a question
4. Or, as an alternative, send a POST request to `http://localhost:5001/ask` with the following JSON body:

```json
{
    "mood": "happy",
    "persona": "yoda",
    "text": "What is human life expectancy in the United States?"
}
```

## Acknowledgements

This project was inspired by the following projects:

- OpenAI API
- Coquis-TTS
