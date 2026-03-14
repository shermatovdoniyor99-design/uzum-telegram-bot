import requests
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
UZUM_API_KEY = os.getenv("UZUM_API_KEY")

SHOP_ID = [54161, 64857]

previous_orders = 0
previous_revenue = 0


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


def get_stats():

    orders = get_orders()

    total_orders = len(orders)
    revenue = 0

    for o in orders:
        for item in o["items"]:
            price = item["price"]
            qty = item["quantity"]
            revenue += price * qty

    return total_orders, revenue


send("🚀 Uzum Analytics bot ishga tushdi")

while True:

    try:

        total_orders, revenue = get_stats()

        global previous_orders
        global previous_revenue

        new_orders = total_orders - previous_orders
        new_revenue = revenue - previous_revenue

        report = f"""
📊 Soatlik Uzum hisoboti

🆕 Yangi buyurtmalar: {new_orders}
💰 Yangi tushum: {new_revenue} so'm

📦 Jami buyurtmalar: {total_orders}
💵 Jami tushum: {revenue} so'm
"""

        send(report)

        previous_orders = total_orders
        previous_revenue = revenue

    except Exception as e:
        send(f"❌ Xato: {e}")

    time.sleep(3600)
