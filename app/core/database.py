from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

from app.core.models import get_models


class Database:
    client : AsyncIOMotorClient
    database = None


db  = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongo_url)
    db.database = db.client[settings.database_name]

    await init_beanie(
        database= db.database,
        document_models= get_models()
    )

async def close_mongo_connection():
    if db.client:
        db.client.close()

async def get_database():
    return db.database