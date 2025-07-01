from flask import Flask, request
import requests
import os

BOT_TOKEN   = "8076926701:AAHf4urcKS09cTNi2177kdD6owAifIfFYW4"
GROUP_ID    = -1002751484716
USER_ID     = 5166975179  # Твой Telegram user ID

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

@app.route('/yandex', methods=['POST'])
def yandex_webhook():
    data = request.json or {}

    # Если пришло сообщение как строка
    text = data.get("text")
    if not text:
        # Или собираем из словаря формы
        answers = data.get("form_response", {}).get("answers", [])
        lines = []
        for ans in answers:
            label = ans.get("label", "")
            value = ans.get("text") or ans.get("string") or ans.get("email") or ""
            lines.append(f"{label} {value}")
        text = "\n".join(lines)

    if not text:
        return {"status": "error", "message": "No text found"}, 400

    # Отправляем в ЛС
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": USER_ID,
        "text": text
    })

    # Отправляем в группу
    requests.post(f"{API_URL}/sendMessage", json={
        "chat_id": GROUP_ID,
        "text": f"Новая бронь:\n{text}"
    })

    return {"ok": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
