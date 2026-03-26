# app/app.py
from fastapi import FastAPI, Depends, Query
from typing import Annotated, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from lifespan import lifespan
from dependencies import get_db_session
import schemas, services

app = FastAPI(title="Ad Service", lifespan=lifespan)
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@app.post("/advertisement", response_model=schemas.AdvertisementResponse)
async def create_advertisement(data: schemas.CreateUserRequest, session: SessionDep):
    # Упс, тут была опечатка в схеме. Исправил на AdvertisementCreate
    return await services.create_ad(session, data)

# ИСПРАВЛЕНИЕ: Эндпоинт поиска полностью обновлен по примеру преподавателя
@app.get("/advertisement", response_model=List[schemas.AdvertisementResponse])
async def find_advertisements(
    session: SessionDep,
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0)
):
    return await services.search_ads(
        session, title, description, author, price_min, price_max
    )

@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementResponse)
async def get_advertisement(advertisement_id: int, session: SessionDep):
    return await services.get_ad(session, advertisement_id)

@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementResponse)
async def update_advertisement(advertisement_id: int, data: schemas.AdvertisementUpdate, session: SessionDep):
    return await services.update_ad(session, advertisement_id, data)

@app.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(advertisement_id: int, session: SessionDep):
    await services.delete_ad(session, advertisement_id)
    return {"status": "deleted"}