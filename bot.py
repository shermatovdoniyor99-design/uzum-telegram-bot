import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UZUM_API_KEY = os.getenv("UZUM_API_KEY")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_sales():
    url = "https://api.uzum.uz/seller-api/v1/orders"
    
    headers = {
        "Authorization": UZUM_API_KEY
    }

    r = requests.get(url, headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        count = len(data)
        return f"📦 Bugungi buyurtmalar: {count}"
    else:
        return "❌ Uzum API dan ma'lumot olinmadi"

send("🚀 Uzum analytics bot ishga tushdi!")

while True:
    report = get_sales()
    send(report)
    time.sleep(3600)
