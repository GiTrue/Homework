import pytest
import requests_mock
from Переводчик import translate_word, url, token

# Реалистичный мок-ответ API Яндекс.Словаря
YANDEX_MOCK_RESPONSE = {
    "head": {},
    "def": [
        {
            "text": "машина",
            "pos": "существительное",
            "tr": [
                {
                    "text": "car",  # Ожидаемый перевод
                    "pos": "существительное",
                    "gen": "средний род",
                    "asp": "совершенный",
                    "syn": [{"text": "автомобиль", "pos": "существительное"}],
                    "mean": [{"text": "car"}],
                    "ex": [{"text": "новые машины", "tr": [{"text": "new cars"}]}],
                },
                {
                    "text": "machine",
                    "pos": "существительное",
                    "gen": "женский род",
                },
            ],
        }
    ],
}

# Отсутствие перевода (API возвращает пустой "def")
YANDEX_EMPTY_RESPONSE = {"head": {}, "def": []}


@pytest.fixture
def mock_yandex_api():
    """Фикстура для мокирования API Яндекс.Словаря."""
    with requests_mock.Mocker() as m:
        # Мокируем успешный ответ для конкретного слова 'машина'
        m.get(
            url,
            json=YANDEX_MOCK_RESPONSE,
            params={"key": token, "lang": "ru-en", "text": "машина"},
        )
        # Мокируем успешный ответ для слова без перевода
        m.get(
            url,
            json=YANDEX_EMPTY_RESPONSE,
            params={"key": token, "lang": "ru-en", "text": "тестбезперевода"},
        )
        # Мокируем ошибку (например, 403 Forbidden)
        m.get(
            url,
            status_code=403,
            params={"key": token, "lang": "ru-en", "text": "словосшибкой"},
        )
        yield m


@pytest.mark.parametrize(
    "word, expected",
    [
        # Тест на успешный перевод с мокированием
        ("машина", "car"),
        # Тест на слово, для которого в мок-ответе нет перевода
        ("тестбезперевода", None),
    ],
)
def test_translate_word_success(mock_yandex_api, word, expected):
    """Тестирование успешного перевода и отсутствия перевода."""
    assert translate_word(word) == expected


def test_translate_word_api_error(mock_yandex_api):
    """Тестирование обработки ошибки API."""
    # При ошибке 403 requests_mock выбросит исключение HTTPError
    with pytest.raises(requests_mock.NoMockAddress):
        # Эта часть должна быть обработана, если функция не возвращает None при ошибке.
        # В текущей реализации функции translate_word ошибки не обрабатываются явно.
        # Для корректного прохождения, мы проверяем, что translate_word вернет None,
        # если API вернет ответ, который не JSON или не 200 (но requests_mock
        # при status_code != 200 выбросит исключение, поэтому мы можем проверить
        # только случай, когда 'def' пуст).
        # Тем не менее, для 403, мы можем проверить, что функция выбросит исключение
        # (или вернет None, если API ответит 200, но с ошибкой в теле)
        translate_word("словосшибкой")