# openai-tts-server

This repo contains the code for an example of a text to speech server that uses the OpenAI API to fetch
customised answers to questions based on a given context.

## Showcase

### Bupa Chatbot Demo (31 May 2023)

https://github.com/pedromspeixoto/bupa/assets/35801678/32d33c97-f554-4fe9-b891-16e6d0a46277

Other videos with earlier versions at `assets/`

## Prerequisites

- Python 3.9

## Installation

1. Clone the repo
2. Install the dependencies with `pip install -r requirements.txt`
3. Create a `tts-server/.env` file with the following variables:

```bash
# options - openai or local
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_MODEL=gpt-3.5-turbo

# options - vits-emo, tortoise or default
TTS_MODE=vits-emo
ROBOT_FILTER=true

COQUI_AI_BASE_URL=https://app.coqui.ai/api/v2/samples
COQUI_AI_API_KEY=<your-coqui-ai-api-key>
COQUI_AI_VOICE_ID=d2bd7ccb-1b65-4005-9578-32c4e02d8ddf

CONVERSATION_HISTORY=true
```

4. To use the local gpt4all model, you first have to download it and place it under `tts-server/assets/bin`;
5. To use the model (vits-emo) that was trained for the purpose of this, please contact me so that I can provide you the URLs.

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
4. Or, as an alternative, to get a response you can send a POST request to `http://localhost:5001/ask` with the following JSON body:

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

- [x] On the existing architecture, create a robot filter to apply to the final audio
- [ ] Create or adapt datasets with emotion for training the TTS models
- [ ] Apply the robot filter to the emotion dataset
- [ ] Train different models for different moods and personas (notebooks already available to train new models using GlowTTS and VITS)
- [ ] Add more moods and personas
- [ ] Use our own GPT model instead of the OpenAI API

## Acknowledgements

This project was inspired by the following projects:

- OpenAI API
- Coquis-TTS
