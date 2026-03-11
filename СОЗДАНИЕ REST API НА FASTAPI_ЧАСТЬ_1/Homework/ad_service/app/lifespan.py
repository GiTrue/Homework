# app/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
import models  # Импорт важен для инициализации таблиц

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("Shutting down: Disposing engine...")
    await engine.dispose()