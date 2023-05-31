
# openai-tts-server

This repo contains the code for an example of a text to speech server that uses the OpenAI API to fetch
customised answers to questions based on a given context.

## Showcase

### Bupa Chatbot Demo (31 May 2023)

Note: Please note that there are some "silent" actions within the video to simulate a scenario where a user does not speak with the bot after a certain amount of time. Please do not skip those since you will see a custom message to catch your attention after some period of time.

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

## Text to Speech Training

A different set of models were created to generate speech with emotion. In the end, we found that the best results were achieved by fine tuning an existing VITS model and adding a multi speaker functionality where each of the speakers is an emotion.

The notebook used to train this model is available under `notebooks/` such as the other models that were tested.

There are the results for our TTS model after 1.017.756 steps:

| *Sentence* | Neutral | Angry | Sad | Happy | Surprised
|--|--|--|--|--|--|
| *"I am a crazy scientist."* |[0_mymodel_vits_output_1017756_neutral.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/2e9850a4-509f-4d8a-9df8-c29006626229)|[0_mymodel_vits_output_1017756_angry.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/010e8e5b-c7ae-4236-b777-06559b06c74d)|[0_mymodel_vits_output_1017756_sad.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/2ea674f2-6edd-4783-9edf-5b1752185c9e)|[0_mymodel_vits_output_1017756_happy.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/a9b12c2e-b6f7-4314-ab0d-3af6e6f2ffbd)|[0_mymodel_vits_output_1017756_surprise.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/4a9bff5f-6ae0-45d8-8d94-6976887884fa)|
| *"The cake is a lie."* |[1_mymodel_vits_output_1017756_neutral.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/c09f59d9-7715-451c-9033-e8cde85f9f81)|[1_mymodel_vits_output_1017756_angry.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/cb81ac7b-52a5-43cb-88a3-08b4079b664c)|[1_mymodel_vits_output_1017756_sad.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/e3511823-58fe-4121-a1c0-922044cf700f)|[1_mymodel_vits_output_1017756_happy.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/b6b06436-c470-4314-b61b-47d0ecdad17c)|[1_mymodel_vits_output_1017756_surprise.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/ca3af767-7c37-4bbf-b637-46a8e039a1b1)|
| *"Do you want to go to the supermarket with me?"* |[2_mymodel_vits_output_1017756_neutral.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/c27a1c54-d843-4000-be68-ebde681497c9)|[2_mymodel_vits_output_1017756_angry.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/7a0235c7-409e-4a2e-a831-7a122f49628c)|[2_mymodel_vits_output_1017756_sad.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/843de05c-9716-4988-8d54-c0f836daf9cd)|[2_mymodel_vits_output_1017756_happy.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/e94a02a8-a8be-4b94-a9ba-fa8f292334b7)|[2_mymodel_vits_output_1017756_surprise.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/e19a967e-6d9a-48db-9ffa-a8762f350a82)|
| *"I am feeling great today!"* |[3_mymodel_vits_output_1017756_neutral.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/5d03a4a8-b920-41b2-8ad3-f29448869783)|[3_mymodel_vits_output_1017756_angry.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/68f9572c-3fcf-44d4-b052-75db63c8899f)|[3_mymodel_vits_output_1017756_sad.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/0e6ea311-2ad9-42b9-b0e7-12ee0ac8c16a)|[3_mymodel_vits_output_1017756_happy.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/4db92bfe-8332-4c3d-a443-3181149af1e5)|[3_mymodel_vits_output_1017756_surprise.webm](https://github.com/pedromspeixoto/bupa/assets/35801678/38c11394-8255-452e-b450-44a5ee1646e5)|

## Robot Filters

The filters were designed by a post production sound designer and applied using a set of Python libraries (kudos to Spotify [Pedalboard](https://github.com/spotify/pedalboard) librart).

## Next steps

- [x] On the existing architecture, create a robot filter to apply to the final audio
- [x] Create or adapt datasets with emotion for training the TTS models
- [x] Apply the robot filter to the emotion dataset
- [x] Train different models for different moods and personas (notebooks already available to train new models using GlowTTS and VITS)
- [ ] Add more moods and personas
- [ ] Use our own GPT model instead of the OpenAI API

## Acknowledgements

This project was inspired by the following projects:

- OpenAI API
- Coquis-TTS
- Spotify Pedalboard
