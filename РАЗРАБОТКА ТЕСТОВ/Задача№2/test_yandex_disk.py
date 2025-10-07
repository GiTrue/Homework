import pytest
import requests_mock
import time
import os

# Импортируем функции клиента API из соседнего файла
from yandex_api_client import (
    create_yandex_folder, 
    get_yandex_resource_info, 
    delete_yandex_resource, 
    BASE_URL, 
    YANDEX_TOKEN
)

# --- Функциональный тест (требует реальный токен) ---

# Условие для пропуска функциональных тестов, если токен не установлен
SKIP_FUNCTIONAL = (
    os.getenv("YANDEX_TOKEN") is None 
    or YANDEX_TOKEN == "YOUR_YANDEX_TOKEN_PLACEHOLDER"
)

@pytest.fixture(scope="module")
def unique_folder_name():
    """Фикстура для генерации уникального имени папки для каждого запуска."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"TestFolder_{timestamp}"

@pytest.mark.skipif(
    SKIP_FUNCTIONAL,
    reason="Для функциональных тестов требуется реальный YANDEX_TOKEN в переменных окружения."
)
class TestYandexDiskFunctional:

    def test_create_and_verify_folder(self, unique_folder_name):
        """
        Положительный тест: Проверка создания и существования папки.
        """
        
        # 1. Создание папки
        creation_response = create_yandex_folder(unique_folder_name)
        assert creation_response.status_code == 201, "Ошибка при создании папки (ожидался 201)."
        
        # 2. Проверка существования папки
        verification_response = get_yandex_resource_info(unique_folder_name)
        assert verification_response.status_code == 200, "Папка не найдена после создания (ожидался 200)."
        assert verification_response.json().get('type') == 'dir', "Созданный ресурс не является папкой."
        
        # 3. Очистка (удаление папки)
        delete_response = delete_yandex_resource(unique_folder_name)
        assert delete_response.status_code == 202, "Ошибка при удалении папки (очистка)."


# --- Юнит-тесты (с мокированием) ---

MOCK_FOLDER_PATH = "MyMockFolder"
MOCK_HEADERS = {'Authorization': f'OAuth {YANDEX_TOKEN}', 'Accept': 'application/json'}

@pytest.fixture
def mock_yandex_disk():
    """Фикстура для мокирования API Яндекс.Диска."""
    with requests_mock.Mocker() as m:
        yield m

@pytest.mark.parametrize(
    "status_code, expected_status_code, test_name",
    [
        (201, 201, "Положительный: Успешное создание (201)"),
        (409, 409, "Отрицательный: Папка уже существует (409 Conflict)"), 
        (401, 401, "Отрицательный: Ошибка авторизации (401 Unauthorized)"),
        (400, 400, "Отрицательный: Неверные данные (400 Bad Request)"),
        (507, 507, "Отрицательный: Серверная ошибка (507 Insufficient Storage)")
    ]
)
def test_create_folder_response_codes_mocked(
    mock_yandex_disk, status_code, expected_status_code, test_name
):
    """
    Тестирование функции создания папки на различные HTTP-коды ответа API с мокированием.
    """
    # Мокирование PUT-запроса
    mock_yandex_disk.put(
        BASE_URL,
        status_code=status_code,
        headers=MOCK_HEADERS,
        json={"message": f"Mock response for {status_code}"}, 
        params={'path': MOCK_FOLDER_PATH}
    )
    
    response = create_yandex_folder(MOCK_FOLDER_PATH)
    
    # Проверка кода ответа
    assert response.status_code == expected_status_code, (
        f"Тест '{test_name}' не пройден. Ожидался код {expected_status_code}, получен {response.status_code}."
    )