import os
import requests
import time

BOT_TOKEN = os.getenv("8610072960:AAGz0rK3wI9G2d6dlMSxhcIyJ8xDWlfBdY8")
CHAT_ID = os.getenv("711983281")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

send_message("✅ Uzum bot serverda ishga tushdi!")

while True:
    send_message("📊 Uzum bot ishlayapti")
    time.sleep(3600)
