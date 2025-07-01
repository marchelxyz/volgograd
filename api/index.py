from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = os.environ.get("GROUP_CHAT_ID")
USER_ID = os.environ.get("USER_CHAT_ID")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/', methods=['POST'])
def handler():
    data = request.json or {}

    text = data.get("text")
    if not text:
        answers = data.get("form_response", {}).get("answers", [])
        lines = []
        for ans in answers:
            label = ans.get("label", "")
            value = ans.get("text") or ans.get("string") or ans.get("email") or ""
            lines.append(f"{label} {value}")
        text = "\n".join(lines)

    if not text:
        return {"error": "no text"}, 400

    requests.post(f"{API_URL}/sendMessage", json={"chat_id": USER_ID, "text": text})
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": GROUP_ID, "text": f"Новая бронь:\n{text}"})

    return {"status": "ok"}
