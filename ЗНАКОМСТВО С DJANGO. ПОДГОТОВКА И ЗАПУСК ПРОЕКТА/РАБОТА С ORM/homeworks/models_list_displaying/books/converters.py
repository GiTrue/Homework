from datetime import datetime


class DateConverter:
    # Шаблон регулярного выражения для даты ГГГГ-ММ-ДД
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value: str) -> datetime.date:
        # Преобразование строки из URL в объект date
        return datetime.strptime(value, self.format).date()

    def to_url(self, value: datetime.date) -> str:
        # Преобразование объекта date обратно в строку для URL
        return value.strftime(self.format)
