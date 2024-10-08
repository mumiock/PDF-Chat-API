from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client[settings.MONGODB_DB_NAME]
