import os
from flask import Flask, request, jsonify

app = Flask(__name__)

STOAT_BOT_TOKEN = os.getenv("gMolYfXoJyYIXn__HnkrdyRbeXtDqSQBVCY6asQuM1nYy2WaFeW4Y6Pk-LfFxkPV")
TRIGGERS = ["tja brur", "tjo brur"]

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    auth_header = request.headers.get("Authorization", "")

    if STOAT_BOT_TOKEN:
        if auth_header != f"Bearer {STOAT_BOT_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"reply": "Ingen text skickades."})

    for trigger in TRIGGERS:
        if user_message.startswith(trigger):
            question = user_message[len(trigger):].strip()

            if not question:
                return jsonify({"reply": "Vad vill du fråga, brur?"})

            return jsonify({"reply": f"Du frågade: {question}"})

    return jsonify({"reply": "Säg 'tja brur' eller 'tjo brur' först."})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
