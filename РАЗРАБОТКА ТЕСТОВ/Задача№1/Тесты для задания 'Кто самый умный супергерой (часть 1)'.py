import pytest
import requests_mock
from Кто_самый_умный_супергерой__часть_1 import get_the_smartest_superhero

# Мок-ответ API для части 1
ALL_HEROES_MOCK_RESPONSE = [
    {"id": 332, "name": "Hulk", "powerstats": {"intelligence": 81}},
    {"id": 149, "name": "Captain America", "powerstats": {"intelligence": 69}},
    {"id": 659, "name": "Thanos", "powerstats": {"intelligence": 100}},  # Самый умный
    {"id": 70, "name": "Batman", "powerstats": {"intelligence": 88}},  # Игнорируем его
]
URL_ALL_HEROES = "https://akabab.github.io/superhero-api/api/all.json"


@pytest.fixture
def mock_superhero_api_part1():
    """Фикстура для мокирования API всех супергероев."""
    with requests_mock.Mocker() as m:
        m.get(URL_ALL_HEROES, json=ALL_HEROES_MOCK_RESPONSE, status_code=200)
        yield m


def test_get_the_smartest_superhero_part1(mock_superhero_api_part1):
    """Тестирование нахождения самого умного среди заданного списка."""
    # Ожидаемый результат - Thanos, т.к. у него intelligence: 100
    expected_hero = "Thanos"
    assert get_the_smartest_superhero() == expected_hero