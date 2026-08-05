import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "status": "online",
        "service": "Discord AI Messages Assistant"
    }

@app.route("/health")
def health():
    return "OK", 200

def run():
    port = int(os.getenv("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=port,
    )

def start_web_server():
    server = Thread(target=run)
    server.daemon = True
    server.start()