import requests

BASE_URL = "http://127.0.0.1:8080/advertisements"

# Создание
res = requests.post(BASE_URL, json={
    "title": "Aiohttp Adv", 
    "description": "Async is fast", 
    "owner": "admin"
})
print(res.json())
adv_id = res.json().get("id")

# Получение
res = requests.get(f"{BASE_URL}/{adv_id}")
print(res.json())