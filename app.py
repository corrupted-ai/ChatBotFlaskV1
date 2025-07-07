from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

DATABRICKS_ENDPOINT = "https://dummy.databricks.api/endpoint"

EXAMPLE_PROMPTS = {
    "What are your hours of operation?": "Our hours of operation are from 9 AM to 6 PM, Monday to Friday.",
    "Tell me about your pricing model.": "Our pricing is based on usage and starts from $29/month.",
    "How do I reset my password?": "You can reset your password by clicking on the 'Forgot Password' link on the login page."
}

@app.route("/")
def index():
    return render_template("index.html", examples=list(EXAMPLE_PROMPTS.keys()))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    # Simulate specific responses for example prompts
    if user_input in EXAMPLE_PROMPTS:
        reply = EXAMPLE_PROMPTS[user_input]
    else:
        # Dummy call to simulate Databricks endpoint
        # Replace this with actual call logic
        reply = f"Echo: {user_input}"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
