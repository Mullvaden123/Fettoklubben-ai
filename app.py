import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INCEPTION_API_KEY = os.getenv("sk_685262549553b17d8623d1463774131a")
INCEPTION_API_URL = os.getenv("INCEPTION_API_URL", "https://api.inception.ai/v1/chat")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {INCEPTION_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": user_message
    }

    try:
        response = requests.post(INCEPTION_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        # Anpassa detta efter Inceptions faktiska svar
        bot_reply = result.get("reply", "Inget svar från AI")

        return jsonify({"reply": bot_reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
