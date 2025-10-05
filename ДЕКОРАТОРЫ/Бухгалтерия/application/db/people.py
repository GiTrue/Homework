from logger import logger

@logger
def get_employees():
    """Возвращает список сотрудников."""
    print("Получаю список сотрудников...")
    return ["Иванов", "Петров", "Сидоров"]
