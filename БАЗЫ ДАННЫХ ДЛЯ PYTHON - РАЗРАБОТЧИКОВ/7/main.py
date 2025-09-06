import os
from dotenv import load_dotenv
load_dotenv()  # загружает переменные из .env
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Stock, Sale

import os
from dotenv import load_dotenv
load_dotenv()  # загружает переменные из .env

# читаем переменные из среды
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Stock, Sale

DSN = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sa.create_engine(DSN, connect_args={"client_encoding": "utf8"})


Session = sessionmaker(bind=engine)
session = Session()

publisher_input = input("Введите имя или id издателя: ")

query = (
    session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
    .join(Publisher)
    .join(Stock)
    .join(Shop)
    .join(Sale)
)

if publisher_input.isdigit():
    query = query.filter(Publisher.id == int(publisher_input))
else:
    query = query.filter(Publisher.name.ilike(f"%{publisher_input}%"))

for title, shop, price, date in query.all():
    print(f"{title:30} | {shop:15} | {price:6} | {date.strftime('%d-%m-%Y')}")

engine = sa.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

publisher_input = input("Введите имя или id издателя: ")

query = (
    session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
    .join(Publisher)
    .join(Stock)
    .join(Shop)
    .join(Sale)
)

if publisher_input.isdigit():
    query = query.filter(Publisher.id == int(publisher_input))
else:
    query = query.filter(Publisher.name.ilike(f"%{publisher_input}%"))

for title, shop, price, date in query.all():
    print(f"{title:30} | {shop:15} | {price:6} | {date.strftime('%d-%m-%Y')}")



