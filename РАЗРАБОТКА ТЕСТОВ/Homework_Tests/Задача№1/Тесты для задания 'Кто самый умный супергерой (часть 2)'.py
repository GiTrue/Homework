import pytest
import requests_mock
from Кто_самый_умный_супергерой__часть_2 import get_the_smartest_superhero

# Мок-ответы API для части 2 (для запросов по ID)
HERO_MOCKS = {
    # 332: Hulk (intelligence: 81)
    332: {
        "id": 332,
        "name": "Hulk",
        "powerstats": {"intelligence": 81, "power": 80, "combat": 70},
    },
    # 149: Captain America (intelligence: 69)
    149: {
        "id": 149,
        "name": "Captain America",
        "powerstats": {"intelligence": 69, "power": 40, "combat": 100},
    },
    # 659: Thanos (intelligence: 100)
    659: {
        "id": 659,
        "name": "Thanos",
        "powerstats": {"intelligence": 100, "power": 100, "combat": 90},
    },
    # 999: Несуществующий (ошибка)
    999: None,
}
BASE_URL_ID = "https://akabab.github.io/superhero-api/api/id"


@pytest.fixture
def mock_superhero_api_part2():
    """Фикстура для мокирования API супергероев по ID."""
    with requests_mock.Mocker() as m:
        # Мокируем каждый отдельный запрос по ID
        for hero_id, data in HERO_MOCKS.items():
            url = f"{BASE_URL_ID}/{hero_id}.json"
            if data:
                m.get(url, json=data, status_code=200)
            else:
                m.get(url, status_code=404)
        yield m


@pytest.mark.parametrize(
    "superheros_ids, expected_hero",
    [
        # Кейс, где Танос самый умный
        ([332, 149, 659], "Thanos"),
        # Кейс, где Халк самый умный (Таноса нет в списке)
        ([332, 149], "Hulk"),
        # Кейс, где присутствует несуществующий ID (999), который игнорируется
        ([332, 999, 149], "Hulk"),
    ],
)
def test_get_the_smartest_superhero_part2_success(
    mock_superhero_api_part2, superheros_ids, expected_hero
):
    """Тестирование нахождения самого умного среди списка ID."""
    assert get_the_smartest_superhero(superheros_ids) == expected_hero


def test_get_the_smartest_superhero_part2_empty_list(mock_superhero_api_part2):
    """Тестирование пустого списка ID."""
    # Ожидается ошибка, если список пуст, т.к. max() на пустой коллекции вызовет ValueError
    with pytest.raises(ValueError):
        get_the_smartest_superhero([])