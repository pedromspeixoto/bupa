# import all the modules that we will need to use
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import os 
from dotenv import load_dotenv

# load env variables
load_dotenv()

if os.getenv("TTS_MODE") == "default":
    # load the pre existing model
    path = "app/configs/.models.json"
    mm = ModelManager(path)

    # download selected model
    model_path, config_path, model_item = mm.download_model("tts_models/en/ljspeech/tacotron2-DDC")
    voc_path, voc_config_path, _ = mm.download_model(model_item["default_vocoder"])

    # create a synthesizer object
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=voc_path,
        vocoder_config=voc_config_path
    )
    vits_emo_synthesizer = None

elif os.getenv("TTS_MODE") == "vits-emo":
    vits_emo_model_path = "app/assets/vits-emo/model_1017756.pth"
    vits_emo_config_path = "app/assets/vits-emo/config.json"
    vits_emo_speakers_file = "app/assets/vits-emo/speakers.pth"

    # create a custom synthesizer object for our vits-emo model
    vits_emo_synthesizer = Synthesizer(
        tts_checkpoint=vits_emo_model_path,
        tts_config_path=vits_emo_config_path,
        tts_speakers_file=vits_emo_speakers_file
    )

    synthesizer = None

else:
    synthesizer = None
    vits_emo_synthesizer = None