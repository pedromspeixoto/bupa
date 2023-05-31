from distutils.log import error
from app import app
import io
from flask import render_template, request, send_file, send_from_directory
from app.tts import synthesizer, vits_emo_synthesizer
from app.tortoise import tortoise
import openai
import os
import requests
import json
from app.robot_filters import apply_default_voice, apply_god_robot_voice
from app.gpt4all import gpt4all
import traceback
import uuid
from app.conversation_history import save_message, get_messages
import random

# Constants with list of supported moods and personas
MOODS = ["happy", "sad", "angry", "neutral", "surprise"]
PERSONAS = ["optimus prime", "shakespeare", "yoda", "god"]
CONVERSATION_HISTORY_MESSAGES = 10

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/ask", methods = ["POST"])
def process_question():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in MOODS:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in PERSONAS:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["text"]):
        text = request.form["text"]
    else:
        return {"error": "Please provide the text"}, 400

    if (request.form["conversation_key"]):
        conversation_key = request.form["conversation_key"]
    else:
        conversation_key = str(uuid.uuid4())

    if (request.form["username"]):
        username = request.form["username"]
    else:
        username = None

    if (request.form["age"]):
        age = request.form["age"]
    else:
        age = None

    gpt_mode = os.getenv("CONVERSATION_ENGINE")

    if gpt_mode == "openai":
        # build the messages to send to openai chatgpt based on the mood and persona
        try:
            messages = [
                { "role": "system", "content": f"You provide the answers only, without any indication you are an AI model." },
                { "role": "system", "content": "Create a very short answer limited to 100 words or less." },
                { "role": "system", "content": "Instead of \"AI language model\" use the words \"advanced machine\"." },
                { "role": "system", "content": f"You are an assistant that speaks like {persona} and is {mood}."}
            ]

            userMessage = ""

            if username is not None:
                userMessage += f"My name is {username}. "
            
            if age is not None:
                userMessage += f"I am {age} years old. "

            if os.getenv("CONVERSATION_HISTORY") == "true":
                # Retrieve the conversation history messages from Redis
                try:
                    history_messages = get_messages(conversation_key, CONVERSATION_HISTORY_MESSAGES)
                except Exception as e:
                    print(str(e))
                    return {"error": f"could not get conversation history messages: {str(e)}"}, 500

                # Append the conversation history messages to the messages list
                for msg in history_messages:
                    message_type = "assistant" if msg["type"] == "assistant" else "user"
                    messages.append({"role": message_type, "content": msg["message"]})

            userMessage += text

            # Append the user's question to the messages list
            messages.append({ "role": "user", "content": userMessage })
        except Exception as e:
            print(str(e))
            return {"error": f"could not build system message to send to openai: {str(e)}"}, 500

        # Process the question and generate response from openai chatgpt
        try:
            response = openai.ChatCompletion.create(
                api_key=os.getenv("OPENAI_API_KEY"),
                model=os.getenv("OPENAI_MODEL"),
                messages=messages,
                temperature=0.2
            )

            answer = response.choices[0].message["content"]
            #answer = "Bien gracias y tu? I am feeling wonderful!"

            # Save the question and answer to Redis
            if os.getenv("CONVERSATION_HISTORY") == "true":
                try:
                    save_message(conversation_key, "user", text)
                    save_message(conversation_key, "assistant", answer)
                except Exception as e:
                    print(f"error. could not save question and answer to conversation history: {str(e)}")

            return {"conversation_key": conversation_key, "answer": answer}, 200
        except Exception as e:
            return {"error": f"could not get response from openai: {str(e)}"}, 500
    
    elif gpt_mode == "local":
        # build the messages to send to local gpt4all model based on the mood and persona
        try:
            messages = [
                { "role": "system", "content": f"You are an assistant that speaks like {persona} and is {mood}."},
                { "role": "system", "content": "Create a very short answer limited to 100 words or less." },
                { "role": "system", "content": "Instead of \"AI language model\" use the words \"advanced machine\"." },
                { "role": "user", "content": text}
            ]
            answer = gpt4all.chat_completion(messages)
            return {"answer": answer['choices'][0]['message']['content']}, 200
        except Exception as e:
            print(str(e))
            return {"error": f"could not build system message to send to local gpt4all: {str(e)}"}, 500
    else:
        return {"error": "gpt mode not supported"}, 400

@app.route("/reminder", methods = ["POST"])
def generate_reminder():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in MOODS:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in PERSONAS:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["username"]):
        username = request.form["username"]
    else:
        return {"error": "Please provide the user name"}, 400

    # Fetch a random reminder based on the mood and persona
    reminders_path = f"app/configs/reminders/{persona}/{mood}/reminders.csv"
    try:
        with open(reminders_path, "r") as f:
            reminders = f.readlines()
            reminder = random.choice(reminders).strip()
            # Replace token in string with username
            reminder = reminder.replace("${username}", username)
            return {"answer": reminder}, 200
    except Exception as e:
        return {"error": f"could not get reminder: {str(e)}"}, 500

@app.route("/greeting", methods = ["POST"])
def generate_greeting():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in MOODS:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in PERSONAS:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["username"]):
        username = request.form["username"]
    else:
        return {"error": "Please provide the user name"}, 400

    # Fetch a random greeting based on the mood and persona
    greetings_path = f"app/configs/greetings/{persona}/{mood}/greetings.csv"
    try:
        with open(greetings_path, "r") as f:
            greetings = f.readlines()
            greeting = random.choice(greetings).strip()
            # Replace token in string with username
            greeting = greeting.replace("${username}", username)
            return {"answer": greeting}, 200
    except Exception as e:
        return {"error": f"could not get greeting: {str(e)}"}, 500

@app.route("/goodbye", methods = ["POST"])
def generate_goodbye():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in MOODS:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in PERSONAS:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["username"]):
        username = request.form["username"]
    else:
        return {"error": "Please provide the user name"}, 400

    # Fetch a random greeting based on the mood and persona
    goodbyes_path = f"app/configs/goodbyes/{persona}/{mood}/goodbyes.csv"
    try:
        with open(goodbyes_path, "r") as f:
            goodbyes = f.readlines()
            goodbye = random.choice(goodbyes).strip()
            # Replace token in string with username
            goodbye = goodbye.replace("${username}", username)
            return {"answer": goodbye}, 200
    except Exception as e:
        return {"error": f"could not get goodbye: {str(e)}"}, 500

@app.route("/audio", methods = ["POST"])
def generate_audio():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in MOODS:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in PERSONAS:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["text"]):
        text = request.form["text"]
    else:
        return {"error": "Please provide the text"}, 400

    # process answer to speech
    tts_mode = os.getenv("TTS_MODE")
    robot_filter = os.getenv("ROBOT_FILTER")

    try:
        out = process_text_to_speech(text, persona, mood, tts_mode, robot_filter)
        return send_file(out, mimetype="audio/wav")
    except Exception as e:
        # printing stack trace
        traceback.print_exc()
        print(str(e))
        return {"error": f"could not synthetise response from answer: {str(e)}"}, 500

def process_text_to_speech(text, persona, mood, tts_mode="vits-emo", robot_filter="true"):
    # process answer to speech
    try:
        # Main supported method
        if tts_mode == "vits-emo":
            outputs = vits_emo_synthesizer.tts(text=text, speaker_name=mood)
            out = io.BytesIO()
            vits_emo_synthesizer.save_wav(outputs, out)

            # Apply robot voice filter based on persona
            if robot_filter == "true":
                if persona == "god":
                    robot_output = apply_god_robot_voice(io.BytesIO(out.getvalue()))
                    return io.BytesIO(robot_output)
                else:
                    robot_output = apply_default_voice(io.BytesIO(out.getvalue()))
                    return io.BytesIO(robot_output)

            return out

        elif tts_mode == "coquiai":                                    
            # Adapt emotion to have first letter capitalized
            emotion = mood.capitalize()

            # Read environment variables
            url = os.getenv("COQUI_AI_BASE_URL")
            bearer_token = os.getenv("COQUI_AI_API_KEY")
            voice_id = os.getenv("COQUI_AI_VOICE_ID")

            # Request headers
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {bearer_token}",
                "content-type": "application/json",
            }

            # Request payload
            payload = {
                "emotion": emotion,
                "speed": 1.2,
                "text": text,
                "voice_id": voice_id,
            }

            # Convert payload to JSON format
            data = json.dumps(payload)

            # Send POST request
            response = requests.post(url, headers=headers, data=data)

            # Get the response content
            response_content = response.json()

            # Check if the response is successful
            if response.status_code != 201:
                return {"error": response_content["detail"]}, response.status_code

            # Download file and return it
            response_data = response.json()
            audio_url = response_data["audio_url"]

            # Download the audio file and serve it
            response = requests.get(audio_url)

            # Apply robot voice filter
            if robot_filter == "true":
                robot_output = apply_robot_voice(io.BytesIO(response.content))
                return io.BytesIO(robot_output)

            return io.BytesIO(response.content)

        elif tts_mode == "tortoise":
            out = io.BytesIO()
            tortoise.tts_to_file(
                text=f"{text}",
                voice_dir="app/assets/tortoise/voices/",
                file_path=out,
                speaker=f"eds-{mood}",
                num_autoregressive_samples=1,
                diffusion_iterations=10
            )

            # Apply robot voice filter
            if robot_filter == "true":
                robot_output = apply_robot_voice(io.BytesIO(out.getvalue()))
                return io.BytesIO(robot_output)

            return out

        elif tts_mode == "default":
            outputs = synthesizer.tts(text)
            out = io.BytesIO()
            synthesizer.save_wav(outputs, out)

            # Apply robot voice filter
            if robot_filter == "true":
                robot_output = apply_robot_voice(io.BytesIO(out.getvalue()))
                return io.BytesIO(robot_output)

            return out
        
        else:
            raise Exception(f"tts mode not supported")
    except Exception as e:
        # printing stack trace
        traceback.print_exc()
        raise Exception(f"could not synthetise response from answer: {str(e)}")