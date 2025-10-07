Задание «Кто самый умный супергерой (часть 1)?»
Условие задачи
Этот тренажёр позволит вам усовершенствовать навыки работы с файловой системой в Python.

Есть API (https://akabab.github.io/superhero-api/api/) по информации о супергероях с информацией по всем супергероям.

Напишите функцию для определения самого умного супергероя среди Hulk, Captain America, Thanos.



import requests

def get_the_smartest_superhero() -> str:
    # URL API для получения данных о всех супергероях
    url = "https://akabab.github.io/superhero-api/api/all.json"
    # Отправляем GET-запрос к API
    response = requests.get(url)
    # Преобразуем ответ в формат JSON
    heroes = response.json()
    
    # Список супергероев, среди которых нужно найти самого умного
    target_heroes = ['Hulk', 'Captain America', 'Thanos']
    # Словарь для хранения пар "имя супергероя: уровень интеллекта"
    hero_intelligence = {}
    
    # Проходим по всем супергероям из API
    for hero in heroes:
        # Если текущий супергерой есть в нашем списке
        if hero['name'] in target_heroes:
            # Добавляем в словарь пару "имя: уровень интеллекта"
            hero_intelligence[hero['name']] = hero['powerstats']['intelligence']
    
    # Находим супергероя с максимальным значением интеллекта
    # max() возвращает пару (имя, интеллект), [0] берет только имя
    the_smartest_superhero = max(hero_intelligence.items(), key=lambda x: x[1])[0]
    return the_smartest_superhero