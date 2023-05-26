# openai-tts-server

This repo contains the code for an example of a text to speech server that uses the OpenAI API to fetch
customised answers to questions based on a given context.

## Showcase

### (1.1) Demo as of 26 May 2023

(to be added)

### (1.0) Demo as of 29 April 2023

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

TTS_MODE=coqui-ai

COQUI_AI_BASE_URL=https://app.coqui.ai/api/v2/samples/from-prompt/
COQUI_AI_API_KEY=<your-coqui-ai-api-key>
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

4. Also, to get the speech representation of a text you can send a POST request to `http://localhost:5001/audio` with the following JSON body:

```json
{
    "mood": "happy",
    "persona": "yoda",
    "text": "The human expectancy in the United States fortunately is 78 years old."
}
```

### Using Docker

1. Build the Docker image with `docker build -t bupa-bot .`
2. Run the Docker container with `docker run -p 5001:8080 bupa-bot`
3. Access the server running at `http://localhost:5001/`, configure the Bopa bot and submit a question
4. Or, as an alternative, to get a response you can send a POST request to `http://localhost:5001/answer` with the following JSON body:

```json
{
    "mood": "happy",
    "persona": "yoda",
    "text": "What is human life expectancy in the United States?"
}
```

5. Also, to get the speech representation of a text you can send a POST request to `http://localhost:5001/audio` with the following JSON body:

```json
{
    "mood": "happy",
    "persona": "yoda",
    "text": "The human expectancy in the United States fortunately is 78 years old."
}
```

## Next steps

- [ ] On the existing architecture, create a robot filter to apply to the final audio
- [ ] Create or adapt datasets with emotion for training the TTS models
- [ ] Apply the robot filter to the emotion dataset
- [ ] Train different models for different moods and personas (notebooks already available to train new models using GlowTTS and VITS)
- [ ] Add more moods and personas
- [ ] Use our own GPT model instead of the OpenAI API

## Acknowledgements

This project was inspired by the following projects:

- OpenAI API
- Coquis-TTS
