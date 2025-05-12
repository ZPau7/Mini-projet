import os
from flask import Flask
from datetime import datetime
from flask import request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    return {"status": "ok"}

@app.route("/hello")
def hello():
    return "Hello from cloud run ! 🚀"

@app.route("/status", methods=["GET"])
def status():
    return {"status": "ok", "server_time": datetime.utcnow()}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
