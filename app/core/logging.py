import logging
from app.services.log_service import store_log
import asyncio


class AsyncMongoDBHandler(logging.Handler):
    def emit(self, record):
        asyncio.create_task(self._emit_async(record))

    async def _emit_async(self, record):
        await store_log(
            level=record.levelname,
            message=self.format(record),
            module=record.module,
            func_name=record.funcName,
            line_no=record.lineno,
        )


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # MongoDB handler
    mongo_handler = AsyncMongoDBHandler()
    mongo_handler.setFormatter(formatter)

    logger.addHandler(mongo_handler)

    return logger


logger = setup_logging()
