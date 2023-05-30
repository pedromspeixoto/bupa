from TTS.api import TTS
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

if os.getenv("TTS_MODE") == "tortoise":
    tortoise = TTS("tts_models/en/multi-dataset/tortoise-v2")
else:
    tortoise = None