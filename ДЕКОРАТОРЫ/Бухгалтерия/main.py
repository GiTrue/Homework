from application.salary import calculate_salary
from application.db.people import get_employees
from datetime import date
from logger import logger

@logger
def main():
    """Главная функция программы 'Бухгалтерия'."""
    print(f"Сегодня: {date.today()}")
    employees = get_employees()
    print("Сотрудники:", ', '.join(employees))
    salary = calculate_salary()
    print("Зарплата:", salary)

if __name__ == '__main__':
    main()
    print("\n✅ Программа выполнена успешно. Проверь файл 'main.log'.")
