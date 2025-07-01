import os
import json
from telegram import Bot
from telegram.error import TelegramError

bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    try:
        data = request.json()
        message = data.get("text", "")
        bot.send_message(chat_id=chat_id, text=message)

        return {
            "statusCode": 200,
            "body": "Message sent to Telegram!"
        }
    except TelegramError as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }
