import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("GROUP_CHAT_ID")

def handler(request):
    body = request.get_data(as_text=True)
    
    if not body:
        return {"statusCode": 400, "body": "Empty body"}

    text = f"Новая бронь:\n{body}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload)

    return {
        "statusCode": 200,
        "body": "Sent to Telegram!" if r.status_code == 200 else "Failed"
    }