Старковimport json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:12345@localhost:5432/book_db"
engine = sa.create_engine(DSN)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open("tests_data.json", "r", encoding="utf-8") as fd:
    data = json.load(fd)

model_map = {
    "publisher": Publisher,
    "shop": Shop,
    "book": Book,
    "stock": Stock,
    "sale": Sale,
}

for record in data:
    model = model_map[record["model"]]
    session.add(model(id=record["pk"], **record["fields"]))

session.commit()
print("✅ База успешно заполнена данными!")
