from gpt4all import GPT4All
import os

if os.getenv("GPT_MODE") == "local":
    gpt4all = GPT4All('ggml-gpt4all-j-v1.3-groovy.bin', model_path='./bin/')
else:
    gpt4all = None