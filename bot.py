import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UZUM_API_KEY = os.getenv("UZUM_API_KEY")

SHOP_ID = [54161, 64857]

last_update = None


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })


def get_orders():

    url = "https://api-seller.uzum.uz/api/seller-openapi/v2/fbs/orders"

    headers = {
        "Authorization": f"Bearer {UZUM_API_KEY}",
        "Accept": "application/json"
    }

    params = {
        "shopIds": SHOP_ID,
        "page": 0,
        "size": 50
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    orders = data.get("payload", {}).get("orders", [])

    return orders


def get_report():

    orders = get_orders()

    total_orders = len(orders)
    revenue = 0

    for o in orders:
        for item in o["items"]:
            revenue += item["price"] * item["quantity"]

    return f"""
📊 Uzum sotuv hisoboti

📦 Buyurtmalar: {total_orders}
💰 Tushum: {revenue} so'm
"""


def check_updates():
    global last_update

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    r = requests.get(url).json()

    for update in r["result"]:

        update_id = update["update_id"]

        if last_update is None:
            last_update = update_id
            continue

        if update_id > last_update:

            last_update = update_id

            if "message" in update:

                text = update["message"].get("text", "")

                if text == "/start":
                    send("🤖 Uzum Analytics Bot ishlayapti\n/sales - Bugungi savdo")

                if text == "/sales":
                    send(get_report())


while True:
    try:
        check_updates()
    except Exception as e:
        print("Error:", e)

    time.sleep(5)
