# import all the modules that we will need to use
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import os 

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