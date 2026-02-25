import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:5000"
USER_DATA = {"email": "test@mail.com", "password": "secret_password"}
AUTH = HTTPBasicAuth(USER_DATA["email"], USER_DATA["password"])

# 1. Регистрация пользователя
res = requests.post(f"{BASE_URL}/users", json=USER_DATA)
print("Reg User:", res.json())

# 2. Создание объявления (нужна авторизация)
res = requests.post(f"{BASE_URL}/advertisements", 
                    json={"title": "Задание 2", "description": "С правами доступа"},
                    auth=AUTH)
adv_id = res.json().get("id")
print("Create Adv:", res.json())

# 3. Удаление объявления
res = requests.delete(f"{BASE_URL}/advertisements/{adv_id}", auth=AUTH)
print("Delete Adv:", res.json())