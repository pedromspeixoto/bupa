from gpt4all import GPT4All
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

if os.getenv("apply_god_robot_voice")=="true":
    gpt4all = GPT4All('ggml-gpt4all-j-v1.3-groovy.bin', model_path='./app/assets/bin/')
else:
    gpt4all = None