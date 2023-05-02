from app import app
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    app.run(debug=1, host="::", port="8080")

if __name__ == "__main__":
    main()