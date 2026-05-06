import os
from flask import Flask, request, jsonify

app = Flask(__name__)

TRIGGERS = ["tja brur", "tjo brur"]

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    user_message = data.get("message", "").lower().strip()

    question = None

    for trigger in TRIGGERS:
        if user_message.startswith(trigger):
            question = user_message[len(trigger):].strip()
            break

    if not question:
        return jsonify({"reply": "Säg tja brur eller tjo brur först."})

    # Just nu testar vi bara att svara tillbaka frågan
    reply = f"Du frågade: {question}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
