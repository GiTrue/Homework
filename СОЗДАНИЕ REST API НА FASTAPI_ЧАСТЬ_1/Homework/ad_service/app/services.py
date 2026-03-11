# app/services.py
from fastapi import HTTPException, status
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

async def search_ads(
    session: AsyncSession, 
    title: str = None, 
    author: str = None
):
    stmt = select(models.Advertisement)
    if title:
        stmt = stmt.where(models.Advertisement.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(models.Advertisement.author.ilike(f"%{author}%"))
    
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