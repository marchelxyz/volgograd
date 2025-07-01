import os
from telegram import Bot
from telegram.error import TelegramError
import json

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        data = request.json
        if not data:
            return {"statusCode": 400, "body": "Bad Request: Empty JSON"}

        message = ""
        for key, value in data.items():
            message += f"<b>{key}</b>: {value}\n"

        bot = Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

        return {"statusCode": 200, "body": "Message sent"}

    except TelegramError as e:
        return {"statusCode": 500, "body": f"TelegramError: {e}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Unexpected Error: {str(e)}"}
