from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
current_thread_id = None

def send_message(user_message, thread_id=None):
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global current_thread_id
    user_message = request.json["message"]
    response_data = send_message(user_message, current_thread_id)
    current_thread_id = response_data.get("threadId")
    return jsonify({"response": response_data.get("response")})

if __name__ == "__main__":
    app.run(debug=True)
