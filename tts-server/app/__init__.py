from flask import Flask

app = Flask(__name__)

from app import views

# load env variables
from dotenv import load_dotenv
load_dotenv()