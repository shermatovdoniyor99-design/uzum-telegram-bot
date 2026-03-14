import requests

UZUM_API_KEY = "API_KEYINGIZ"

def get_report():

    url = "https://api-seller.uzum.uz/api/seller-openapi/v2/fbs/orders"

    headers = {
        "Authorization": f"Bearer {UZUM_API_KEY}"
    }

    r = requests.get(url, headers=headers)

    data = r.json()

    orders = data["content"]

    total_orders = len(orders)
    revenue = 0

    for o in orders:
        price = o["price"]
        qty = o["quantity"]

        revenue += price * qty

    return f"""
📊 Bugungi statistika

Buyurtmalar: {total_orders}
Tushum: {revenue} so'm
"""

print(get_report())
