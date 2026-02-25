import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

PG_DSN = os.getenv("PG_DSN", "postgresql+asyncpg://app:secret@localhost:5431/swapi")

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class SwapiPerson(Base):
    __tablename__ = "swapi_people"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)

async def init_db():
    async with engine.begin() as conn:
        # Сначала удаляем старые таблицы (для чистоты теста) и создаем новые
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)