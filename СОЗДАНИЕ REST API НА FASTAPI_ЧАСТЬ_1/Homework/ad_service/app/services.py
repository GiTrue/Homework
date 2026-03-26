# app/services.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas

async def create_ad(session: AsyncSession, ad_data: schemas.AdvertisementCreate):
    new_ad = models.Advertisement(**ad_data.model_dump())
    session.add(new_ad)
    await session.commit()
    await session.refresh(new_ad)
    return new_ad

async def get_ad(session: AsyncSession, ad_id: int):
    ad = await session.get(models.Advertisement, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad

# ИСПРАВЛЕНИЕ: Функция search_ads полностью переписана по примеру преподавателя
async def search_ads(
    session: AsyncSession, 
    title: str = None, 
    description: str = None,
    author: str = None,
    price_min: float = None,
    price_max: float = None
):
    stmt = select(models.Advertisement)
    
    # Расширенный поиск:
    if title:
        stmt = stmt.where(models.Advertisement.title.ilike(f"%{title}%"))
    if description:
        stmt = stmt.where(models.Advertisement.description.ilike(f"%{description}%"))
    if author:
        stmt = stmt.where(models.Advertisement.author.ilike(f"%{author}%"))
    if price_min:
        stmt = stmt.where(models.Advertisement.price >= price_min)
    if price_max:
        stmt = stmt.where(models.Advertisement.price <= price_max)
    
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_ad(session: AsyncSession, ad_id: int, ad_data: schemas.AdvertisementUpdate):
    ad = await get_ad(session, ad_id)
    for key, value in ad_data.model_dump(exclude_unset=True).items():
        setattr(ad, key, value)
    await session.commit()
    await session.refresh(ad)
    return ad

async def delete_ad(session: AsyncSession, ad_id: int):
    ad = await get_ad(session, ad_id)
    await session.delete(ad)
    await session.commit()