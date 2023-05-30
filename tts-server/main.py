from app import app
import os
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

def main():
    load_dotenv()
    http_server = WSGIServer(("::", 8080), app)
    http_server.serve_forever()

if __name__ == "__main__":
    main()