import requests

url = "https://api-seller.uzum.uz/api/seller-openapi/v2/fbs/orders"

headers = {
    "Authorization": "API_KEY"
}

params = {
    "shopIds": 54161,
    "page": 0,
    "size": 20
}

r = requests.get(url, headers=headers, params=params)

print(r.json())
