import json
import os
from telegram import Bot, TelegramError

def handler(request):
    try:
        data = request.get_json()

        name = data.get("Имя", "Без имени")
        phone = data.get("Телефон", "Без телефона")
        date = data.get("Дата", "")
        time1 = data.get("Время 03.07", "")
        time2 = data.get("Время 04.07", "")
        guests = data.get("Кол-во гостей", "")
        form_url = data.get("Ссылка на форму", "")

        # Собираем сообщение
        message = (
            f"📥 Новая заявка на открытие:\n"
            f"👤 Имя: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"📅 Дата: {date}\n"
            f"⏰ Время 03.07: {time1}\n"
            f"⏰ Время 04.07: {time2}\n"
            f"👥 Гостей: {guests}\n"
            f"🔗 Форма: {form_url}"
        )

        bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
        bot.send_message(chat_id=os.environ["TELEGRAM_CHAT_ID"], text=message)

        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True})
        }

    except TelegramError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
