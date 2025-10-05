from datetime import datetime

def logger(old_function):
    """Декоратор, записывающий вызовы функций в общий файл main.log."""
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        log_message = (
            f"{datetime.now()} — "
            f"Функция '{old_function.__name__}' вызвана с аргументами: "
            f"args={args}, kwargs={kwargs}. "
            f"Результат: {result}\n"
        )
        with open('main.log', 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return result
    return new_function
