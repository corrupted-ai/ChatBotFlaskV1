from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


EXAMPLE_PROMPTS = [
    "What is a Boss Order?",
    "Can Spirit Employee Use discount in Spencer Store?",
    "What to do if someone is injured in store?",
]


@app.route("/")
def index():
    return render_template("index.html", examples=EXAMPLE_PROMPTS)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json().get("message", [])
    model = request.get_json().get("model", "gpt4o") 
    if model == "claude":
        endpoint = "claude-storeassistant"  # Replace with your actual Claude endpoint
    else:
        endpoint = "openai-storeassistant"

    url = f'https://{os.getenv("DATABRICKS_HOST")}/serving-endpoints/{endpoint}/invocations'

    headers = {'Authorization': f'Bearer {os.getenv("DATABRICKS_TOKEN")}', 'Content-Type': 'application/json'}
    json_data ={"messages": user_input}
    json_str = json.dumps(json_data)
    # print(user_input)
    response = requests.request(method='POST', headers=headers, url=url, data=json_str)

    # return jsonify({"reply": reply})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
