import os
from flask import Flask
from datetime import datetime
from flask import request, jsonify
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai
from utils.gcs_utils import read_data, append_data

app = Flask(__name__)

# Initialisation de Vertex AI
vertexai.init(project="rock-drake-459218-i5", location="europe-west1")
model = GenerativeModel(model_name="gemini-2.0-flash-001")
chat: ChatSession = model.start_chat()

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "ok"}

@app.route("/data", methods=["GET"])
def get_data():
    try:
        data = read_data()
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/data", methods=["POST"])
def post_data():
    try:
        new_row = request.get_json()
        append_data(new_row)
        return {"message": "Data added successfully"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/hello")
def hello():
    return "Hello from cloud run ! 🚀"

@app.route("/status", methods=["GET"])
def status():
    return {"status": "ok", "server_time": datetime.utcnow()}

@app.route("/joke", methods=["GET"])
def generate_joke():
    try:
        response = chat.send_message("Raconte-moi une blague drôle.")
        return jsonify({"joke": response.text})
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
