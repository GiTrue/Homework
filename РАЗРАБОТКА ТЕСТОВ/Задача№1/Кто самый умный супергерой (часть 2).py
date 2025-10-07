Условие задачи
Работа с этим тренажёром поможет вам отработать навыки:
· Работы с внешними API: формирование запросов и обработка HTTP-ответов.
· Парсинга JSON: извлечение вложенных полей и структурирование данных.
· Организации данных в Python: использование словарей для хранения результатов.

Есть API (https://akabab.github.io/superhero-api/api/) по информации о супергероях с информацией по всем супергероям. Теперь нужно найти самого умного супергероя среди списка супергероев.

Напишите функцию get_the_smartest_superhero, которая принимает на вход список superheros, состоящий из id.




import requests

def get_the_smartest_superhero(superheros):
    # Создаем словарь для хранения пар "имя супергероя: уровень интеллекта"
    hero_intelligence = {}
    
    # Проходим по каждому ID супергероя в списке
    for hero_id in superheros:
        # Формируем URL для получения информации о конкретном супергерое
        url = f"https://akabab.github.io/superhero-api/api/id/{hero_id}.json"
        
        # Отправляем GET-запрос к API
        response = requests.get(url)
        
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Преобразуем ответ в формат JSON
            hero_data = response.json()
            
            # Получаем имя и уровень интеллекта супергероя
            hero_name = hero_data['name']
            intelligence = hero_data['powerstats']['intelligence']
            
            # Добавляем в словарь пару "имя: уровень интеллекта"
            hero_intelligence[hero_name] = intelligence
    
    # Находим супергероя с максимальным значением интеллекта
    # max() возвращает пару (имя, интеллект), [0] берет только имя
    the_smartest_superhero = max(hero_intelligence.items(), key=lambda x: x[1])[0]
    
    return the_smartest_superhero
