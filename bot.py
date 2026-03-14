import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UZUM_API_KEY = os.getenv("UZUM_API_KEY")

SHOP_ID = [54161, 64857]

last_orders = 0
last_revenue = 0


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })


def get_orders():

    url = "https://api-seller.uzum.uz/api/seller-openapi/v1/finance/orders"

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

    return data.get("payload", {}).get("orders", [])


def get_stats():

    orders = get_orders()

    total_orders = len(orders)
    revenue = 0

    for o in orders:
        for item in o["items"]:
            revenue += item["price"] * item["quantity"]

    return total_orders, revenue


send("🚀 Uzum analytics bot ishga tushdi")

while True:

    try:

        total_orders, revenue = get_stats()

        new_orders = total_orders - last_orders
        new_revenue = revenue - last_revenue

        report = f"""
📊 Soatlik Uzum hisoboti

🆕 Yangi buyurtmalar: {new_orders}
💰 Yangi tushum: {new_revenue} so'm

📦 Jami buyurtmalar: {total_orders}
💵 Jami tushum: {revenue} so'm
"""

        send(report)

        last_orders = total_orders
        last_revenue = revenue

    except Exception as e:
        print(e)

    time.sleep(3600)
