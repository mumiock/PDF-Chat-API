from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from datetime import datetime
import logging

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]
log_collection = db["logs"]

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def store_log(
    level: str, message: str, module: str, func_name: str, line_no: int
):
    log_entry = {
        "timestamp": datetime.utcnow(),
        "level": level,
        "message": message,
        "module": module,
        "funcName": func_name,
        "lineNo": line_no,
    }
    await log_collection.insert_one(log_entry)


async def get_logs(limit: int = 100):
    async def format_logs(logs):
        formatted_logs = []
        for log in logs:
            record = logging.LogRecord(
                name=log["module"],
                level=getattr(logging, log["level"]),
                pathname="",
                lineno=log["lineNo"],
                msg=log["message"],
                args=(),
                exc_info=None,
            )
            record.funcName = log["funcName"]
            record.created = log["timestamp"].timestamp()
            formatted_logs.append(formatter.format(record))
        return formatted_logs

    error_logs = (
        await log_collection.find({"level": "ERROR"})
        .sort("timestamp", -1)
        .limit(limit)
        .to_list(length=limit)
    )
    info_logs = (
        await log_collection.find({"level": "INFO"})
        .sort("timestamp", -1)
        .limit(limit)
        .to_list(length=limit)
    )

    return {
        "errors": await format_logs(error_logs),
        "info": await format_logs(info_logs),
    }
