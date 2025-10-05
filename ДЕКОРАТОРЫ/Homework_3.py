Пример импорта и применения декоратора с выводом логов в программе "Бухгалтерия" (см. папку программы).

# logger.py

from application.salary import calculate_salary
from application.db.people import get_employees
from logger import logger  # импортируем твой декоратор

@logger  # применяем декоратор
def main():
    get_employees()
    calculate_salary()

if __name__ == '__main__':
    main()
