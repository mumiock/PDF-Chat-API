from fastapi import FastAPI
from app.api import pdf, chat, logs
from app.core.logging import setup_logging
from app.database import init_db

app = FastAPI(
    title="PDF Chat API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

setup_logging()

app.include_router(pdf.router, prefix="/v1", tags=["pdf"])
app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(logs.router, prefix="/v1", tags=["logs"])


async def startup_event():
    app.state.db = await init_db()


async def shutdown_event():
    pass


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
