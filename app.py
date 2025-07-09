from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

DATABRICKS_ENDPOINT = "https://dummy.databricks.api/endpoint"

EXAMPLE_PROMPTS = [
    "What is a Boss Order?",
    "Can Spirit Employee Use discount in Spencer Store?",
    "What to do if someone is injured in store?",
]

def get_access_token():
    token_url = f"https://{os.environ['DATABRICKS_HOST']}/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ["DATABRICKS_CLIENT_ID"],
        "client_secret": os.environ["DATABRICKS_CLIENT_SECRET"],
        "scope": "all-apis"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

DATABRICKS_TOKEN = get_access_token()

@app.route("/")
def index():
    return render_template("index.html", examples=EXAMPLE_PROMPTS)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json().get("message", [])

    url = f'https://{os.environ["DATABRICKS_HOST"]}/serving-endpoints/openai-storeassistant/invocations'
    headers = {'Authorization': f'Bearer {DATABRICKS_TOKEN}', 'Content-Type': 'application/json'}
    json_data ={"messages": user_input}
    json_str = json.dumps(json_data)
    # print(user_input)
    response = requests.request(method='POST', headers=headers, url=url, data=json_str)

    # return jsonify({"reply": reply})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
