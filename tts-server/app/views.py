from distutils.log import error
from app import app
import io
from flask import render_template, request, send_file, send_from_directory
from app.tts import synthesizer
import openai
import os

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
            temperature=0
        )
        answer = response.choices[0].message["content"]
        print(answer)
    except Exception as e:
        print(str(e))
        return {"error": f"could not get response from openai: {str(e)}"}, 500

    # process answer to speech
    try:
        outputs = synthesizer.tts(answer)
        out = io.BytesIO()
        synthesizer.save_wav(outputs, out)
        return send_file(out, mimetype="audio/wav")
    except Exception as e:
        print(str(e))
        return {"error": f"could not synthetise response from answer: {str(e)}"}, 500