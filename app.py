from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Загружаем токен и ID из переменных среды
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Например: -1001234567890

@app.route("/", methods=["GET"])
def home():
    return "Webhook работает!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return "Нет данных", 400

    # Распарси ответ Яндекс Формы (пример!)
    answers = []
    for item in data.get("form_response", {}).get("answers", []):
        label = item.get("label", "Вопрос")
        text = item.get("text", "Ответ отсутствует")
        answers.append(f"{label}: {text}")

    message = "\n".join(answers)

    # Отправка в Telegram
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, data=payload)

    return "OK", 200
