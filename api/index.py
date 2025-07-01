import os
import json
from http.server import BaseHTTPRequestHandler
from telegram import Bot

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Печатаем в лог полученный JSON
            print("📥 RAW post_data:", post_data)

            try:
                payload = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"❌ Invalid JSON")
                return

            # Если это данные из Яндекс.Формы — собираем из параметров
            name = payload.get("Имя", "Неизвестно")
            phone = payload.get("Телефон", "Неизвестно")

            message = f"📨 Новая заявка:\nИмя: {name}\nТелефон: {phone}"

            bot = Bot(token=BOT_TOKEN)
            bot.send_message(chat_id=CHAT_ID, text=message)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"✅ Message sent")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
