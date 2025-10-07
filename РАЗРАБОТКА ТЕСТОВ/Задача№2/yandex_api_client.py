import requests
import os

# ⚠️ ВНИМАНИЕ: Для функционального теста необходимо установить 
# переменную окружения YANDEX_TOKEN с вашим реальным токеном.
# В противном случае, будет использоваться заглушка 'YOUR_YANDEX_TOKEN_PLACEHOLDER'.
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN", "YOUR_YANDEX_TOKEN_PLACEHOLDER")
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
HEADERS = {
    # Токен вставляется в заголовок Authorization
    'Authorization': f'OAuth {YANDEX_TOKEN}',
    'Accept': 'application/json'
}

def create_yandex_folder(folder_path):
    """
    Создает папку на Яндекс.Диске и возвращает HTTP-ответ.
    Endpoint: PUT /resources
    """
    params = {'path': folder_path}
    response = requests.put(BASE_URL, headers=HEADERS, params=params)
    return response
    
def get_yandex_resource_info(folder_path):
    """
    Получает информацию о ресурсе на Яндекс.Диске и возвращает HTTP-ответ.
    Endpoint: GET /resources
    """
    params = {'path': folder_path}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    return response

def delete_yandex_resource(folder_path):
    """
    Удаляет ресурс с Яндекс.Диска (перманентно).
    Endpoint: DELETE /resources
    """
    # permanently='true' обеспечивает немедленное удаление без помещения в Корзину.
    params = {'path': folder_path, 'permanently': 'true'} 
    response = requests.delete(BASE_URL, headers=HEADERS, params=params)
    return response