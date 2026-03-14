import requests
import os

UZUM_API_KEY = os.getenv("UZUM_API_KEY")
SHOP_ID = [54161, 64857]

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
            price = item["price"]
            qty = item["quantity"]
            revenue += price * qty

    return f"""
📊 Uzum hisoboti

📦 Buyurtmalar: {total_orders}
💰 Tushum: {revenue} so'm
"""


print(get_report())
