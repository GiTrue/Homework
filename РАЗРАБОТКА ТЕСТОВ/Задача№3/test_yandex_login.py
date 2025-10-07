import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ⚠️ ВАЖНО: Никогда не храните логин и пароль в открытом коде! 
# Для реальных тестов используйте переменные окружения.

# Чтение учетных данных из переменных окружения
# Для запуска теста необходимо установить:
# export YANDEX_LOGIN="ваш_логин"
# export YANDEX_PASSWORD="ваш_пароль"
YANDEX_LOGIN = os.getenv("YANDEX_LOGIN", "TEST_LOGIN_PLACEHOLDER")
YANDEX_PASSWORD = os.getenv("YANDEX_PASSWORD", "TEST_PASSWORD_PLACEHOLDER")

# URL для авторизации
LOGIN_URL = "https://passport.yandex.ru/auth/"
SUCCESS_URL_PART = "passport.yandex.ru/profile" # Ожидаемая часть URL после успешной авторизации

@pytest.fixture(scope="module")
def driver():
    """Фикстура для инициализации и закрытия браузера (Chrome)."""
    # Инициализация Chrome Driver
    # service = webdriver.ChromeService(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service)
    
    # Современный способ инициализации с использованием webdriver_manager
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Раскомментировать для запуска без открытия окна браузера
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10) # Установка неявного ожидания
    
    yield driver
    
    # Закрытие браузера после завершения всех тестов в модуле
    driver.quit()

# ---------------------------------------------------------------------

@pytest.mark.skipif(
    YANDEX_LOGIN == "TEST_LOGIN_PLACEHOLDER" or YANDEX_PASSWORD == "TEST_PASSWORD_PLACEHOLDER",
    reason="Учетные данные не установлены в переменных окружения (YANDEX_LOGIN, YANDEX_PASSWORD)."
)
def test_successful_yandex_login(driver):
    """
    Функциональный тест успешной авторизации на Яндексе.
    """
    
    # 1. Открытие страницы авторизации
    driver.get(LOGIN_URL)
    
    wait = WebDriverWait(driver, 10)
    
    # 2. Ввод логина и нажатие "Войти"
    
    # Ожидание появления поля ввода логина
    login_field = wait.until(
        EC.presence_of_element_located((By.ID, "passp-field-login"))
    )
    login_field.send_keys(YANDEX_LOGIN)
    
    # Кнопка "Войти" после ввода логина
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "passp:sign-in"))
    )
    login_button.click()
    
    # 3. Ввод пароля и нажатие "Войти"
    
    # Ожидание появления поля ввода пароля
    password_field = wait.until(
        EC.presence_of_element_located((By.ID, "passp-field-passwd"))
    )
    password_field.send_keys(YANDEX_PASSWORD)
    
    # Кнопка "Войти" после ввода пароля
    password_button = wait.until(
        EC.element_to_be_clickable((By.ID, "passp:sign-in"))
    )
    password_button.click()
    
    # 4. Проверка успешной авторизации
    
    # Ожидание, пока URL изменится
    wait.until(EC.url_contains(SUCCESS_URL_PART))
    
    # Ассерт на успешный переход на страницу профиля или похожую страницу
    current_url = driver.current_url
    assert SUCCESS_URL_PART in current_url, (
        f"Авторизация не удалась. Текущий URL: {current_url}. "
        f"Ожидалась часть: {SUCCESS_URL_PART}"
    )