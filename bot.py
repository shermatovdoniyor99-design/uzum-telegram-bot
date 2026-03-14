import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UZUM_API_KEY = os.getenv("UZUM_API_KEY")

last_update = 0

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_sales():

    url = "https://api-seller.uzum.uz/api/seller-openapi/v2/fbs/orders"

    headers = {
        "Authorization": f"Bearer {UZUM_API_KEY}"
    }

    params = {
        "page": 0,
        "size": 50
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 200:
        data = r.json()

        orders = data.get("content", [])
        count = len(orders)

        return f"📦 Buyurtmalar soni: {count}"

    else:
        return f"❌ API xato: {r.status_code}\n{r.text}"

def check_updates():
    global last_update

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    r = requests.get(url).json()

    for update in r["result"]:
        update_id = update["update_id"]

        if update_id > last_update:
            last_update = update_id

            if "message" in update:
                text = update["message"].get("text", "")

                if text == "/start":
                    send("🤖 Uzum Analytics Bot ishlayapti!\n/sales - Bugungi savdo")

                if text == "/sales":
                    send(get_sales())

send("🚀 Uzum analytics bot ishga tushdi!")

while True:
    check_updates()
    time.sleep(60)
