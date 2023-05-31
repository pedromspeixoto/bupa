from app import app
import os
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

def main():
    load_dotenv()
    if os.getenv("APP_MODE") == "productions":
        http_server = WSGIServer(("::", 8080), app)
        http_server.serve_forever()
    else:
        # Start the Flask development web server
        app.run(host="::", port=8080, debug=True)

if __name__ == "__main__":
    main()