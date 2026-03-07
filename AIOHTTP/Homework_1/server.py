import json
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from db import Session, Advertisement, init_db, engine
from pydantic import ValidationError
from schema import CreateAdv, UpdateAdv

app = web.Application()

async def get_adv_by_id(session, adv_id):
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise web.HTTPNotFound(text=json.dumps({"error": "not found"}), content_type="application/json")
    return adv

class AdvView(web.View):
    
    async def get(self):
        adv_id = int(self.request.match_info["adv_id"])
        async with Session() as session:
            adv = await get_adv_by_id(session, adv_id)
            return web.json_response(adv.dict)

    async def post(self):
        data = await self.request.json()
        try:
            validated_data = CreateAdv(**data).model_dump()
        except ValidationError as e:
            raise web.HTTPBadRequest(text=e.json(), content_type="application/json")
        
        async with Session() as session:
            adv = Advertisement(**validated_data)
            session.add(adv)
            await session.commit()
            return web.json_response({"id": adv.id})

    async def patch(self):
        adv_id = int(self.request.match_info["adv_id"])
        data = await self.request.json()
        async with Session() as session:
            adv = await get_adv_by_id(session, adv_id)
            for key, value in data.items():
                setattr(adv, key, value)
            session.add(adv)
            await session.commit()
            return web.json_response({"status": "updated"})

    async def delete(self):
        adv_id = int(self.request.match_info["adv_id"])
        async with Session() as session:
            adv = await get_adv_by_id(session, adv_id)
            await session.delete(adv)
            await session.commit()
            return web.json_response({"status": "deleted"})

# Контекст для инициализации БД при старте
async def init_orm(app):
    await init_db()
    yield
    await engine.dispose()

app.cleanup_ctx.append(init_orm)

app.add_routes([
    web.post("/advertisements", AdvView),
    web.get("/advertisements/{adv_id:\d+}", AdvView),
    web.patch("/advertisements/{adv_id:\d+}", AdvView),
    web.delete("/advertisements/{adv_id:\d+}", AdvView),
])

if __name__ == "__main__":
    web.run_app(app, port=8080)