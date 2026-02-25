import asyncio
import aiohttp
from more_itertools import chunked
from models import SwapiPerson, Session, init_db, engine

MAX_CHUNK_SIZE = 10  # Размер пачки для одновременных запросов

async def get_person(person_id, session):
    url = f"https://www.swapi.tech/api/people/{person_id}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if "result" not in data:
                return None
            
            prop = data["result"]["properties"]
            return {
                "id": int(data["result"]["uid"]),
                "name": prop.get("name"),
                "birth_year": prop.get("birth_year"),
                "eye_color": prop.get("eye_color"),
                "gender": prop.get("gender"),
                "hair_color": prop.get("hair_color"),
                "homeworld": prop.get("homeworld"),
                "mass": prop.get("mass"),
                "skin_color": prop.get("skin_color"),
            }
    except Exception as e:
        print(f"Error fetching ID {person_id}: {e}")
        return None

async def insert_to_db(people_data):
    # Фильтруем пустые результаты (где ID не существует в API)
    valid_people = [SwapiPerson(**item) for item in people_data if item is not None]
    if not valid_people:
        return

    async with Session() as session:
        session.add_all(valid_people)
        await session.commit()

async def main():
    # 1. Инициализируем базу данных
    await init_db()
    
    # 2. Создаем сессию для запросов
    async with aiohttp.ClientSession() as session:
        # В SWAPI около 83 персонажей, берем с запасом 100
        for person_ids_chunk in chunked(range(1, 101), MAX_CHUNK_SIZE):
            # Создаем список корутин для пачки ID
            coros = [get_person(pid, session) for pid in person_ids_chunk]
            
            # Выполняем запросы пачкой
            people_results = await asyncio.gather(*coros)
            
            # Запускаем задачу на запись в БД (не блокируя следующую итерацию загрузки)
            asyncio.create_task(insert_to_db(people_results))

    # Ждем завершения всех фоновых задач записи в базу
    current_task = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t is not current_task]
    await asyncio.gather(*tasks)
    
    # Закрываем соединение с движком БД
    await engine.dispose()
    print("Вся загрузка завершена успешно!")

if __name__ == "__main__":
    asyncio.run(main())