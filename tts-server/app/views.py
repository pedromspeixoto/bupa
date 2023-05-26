from distutils.log import error
from app import app
import io
from flask import render_template, request, send_file, send_from_directory
from app.tts import synthesizer
import openai
import os
import requests
import json
from app.robot_filter import apply_robot_voice

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
        if mood not in ["happy", "sad", "angry", "neutral"]:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in ["optimus prime", "shakespeare", "yoda"]:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["text"]):
        text = request.form["text"]
    else:
        return {"error": "Please provide the text"}, 400

    # build the messages to send to chatgpt based on the mood and persona
    try:
        messages = [
            { "role": "system", "content": f"You provide the answers only, without any indication you are an AI model and all answers must have some kind of indication of a {mood} tone and that you are {persona}." },
            { "role": "user", "content": text } 
        ]
        print(messages)
    except Exception as e:
        print(str(e))
        return {"error": f"could not build system message to send to openai: {str(e)}"}, 500

    # process the question and generate response from chatgpt
    try:
        response = openai.ChatCompletion.create(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
            temperature=0.8
        )
        answer = response.choices[0].message["content"]
        #answer = "Feeling angry, I am."

        return {"answer": answer}, 200
    except Exception as e:
        return {"error": f"could not get response from openai: {str(e)}"}, 500


@app.route("/audio", methods = ["POST"])
def generate_audio():
    if(request.form["mood"]):
        mood = request.form["mood"]
        if mood not in ["happy", "sad", "angry", "neutral"]:
            return {"error": "Please provide a valid mood"}, 400
    else:
        return {"error": "Please provide the bot mood"}, 400

    if(request.form["persona"]):
        persona = request.form["persona"]
        if persona not in ["optimus prime", "shakespeare", "yoda"]:
            return {"error": "Please provide a valid persona"}, 400                
    else:
        return {"error": "Please provide the bot persona"}, 400

    if(request.form["text"]):
        text = request.form["text"]
    else:
        return {"error": "Please provide the text"}, 400

    # process answer to speech
    try:
        if os.getenv("TTS_MODE") == "coqui-ai":                                    
            # Adapt emotion to have first letter capitalized
            emotion = mood.capitalize()

            # Read environment variables
            url = os.getenv("COQUI_AI_BASE_URL")
            bearer_token = os.getenv("COQUI_AI_API_KEY")

            # Request headers
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {bearer_token}",
                "content-type": "application/json",
            }

            # Request payload
            payload = {
                "emotion": emotion,
                "speed": 0.8,
                "text": text,
                "prompt": f"A voice that sounds like {persona} and is {mood}"
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
            #audio_url = "https://coqui-prod-creator-app-synthesized-samples.s3.amazonaws.com/samples/21103afc-88dd-46cb-8de4-aa25fee8e611.wav"

            # Download the audio file and serve it
            response = requests.get(audio_url)

            # Apply robot voice filter
            if os.getenv("ROBOT_FILTER") == "true":
                robot_output = apply_robot_voice(io.BytesIO(response.content))

            return send_file(io.BytesIO(robot_output), mimetype="audio/wav")

        elif os.getenv("TTS_MODE") == "default":
            outputs = synthesizer.tts(text)
            out = io.BytesIO()
            synthesizer.save_wav(outputs, out)

            # Apply robot voice filter
            if os.getenv("ROBOT_FILTER") == "true":
                robot_output = apply_robot_voice(io.BytesIO(out.getvalue()))

            return send_file(io.BytesIO(robot_output), mimetype="audio/wav")
        else:
            return {"error": "tts mode not supported"}, 400

    except Exception as e:
        print(str(e))
        return {"error": f"could not synthetise response from answer: {str(e)}"}, 500