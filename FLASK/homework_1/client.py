import requests

BASE_URL = "http://127.0.0.1:5000/advertisements"

# 1. Создание
response = requests.post(BASE_URL, json={
    "title": "Продам гараж",
    "description": "В отличном состоянии, торг уместен",
    "owner": "Александр"
})
print("CREATE:", response.json())
adv_id = response.json().get("id")

# 2. Получение
response = requests.get(f"{BASE_URL}/{adv_id}")
print("GET:", response.json())

# 3. Удаление
response = requests.delete(f"{BASE_URL}/{adv_id}")
print("DELETE:", response.json())