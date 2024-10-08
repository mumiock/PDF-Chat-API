from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]
pdf_collection = db["pdf_documents"]


async def store_pdf_content(pdf_id: str, content: str, filename: str):
    await pdf_collection.insert_one(
        {
            "_id": pdf_id,
            "filename": filename,
            "content": content,
        }
    )


async def get_pdf_content(identifier: str) -> str:
    document = await pdf_collection.find_one({"_id": identifier})

    if not document:
        document = await pdf_collection.find_one({"filename": identifier})

    if document:
        return document["content"]
    return None


async def get_all_pdfs(limit: int):
    cursor = pdf_collection.find({}, {"_id": 1, "filename": 1}).limit(limit)
    return await cursor.to_list(length=limit)
