import os
from dotenv import load_dotenv
import sqlalchemy as sa

# Загружаем переменные окружения
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Формируем DSN
DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = sa.create_engine(DSN)
    conn = engine.connect()
    print("Подключение к базе прошло успешно!")
    conn.close()
except Exception as e:
    print("Ошибка подключения к базе:")
    print(e)
