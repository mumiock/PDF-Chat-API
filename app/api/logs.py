from fastapi import APIRouter, HTTPException, Query
from app.services.log_service import get_logs
from app.core.error_messages import ErrorMessages
from app.core.logging import logger
from app.models.pdf import LogListResponse, LogCategoryResponse, LogEntry

router = APIRouter()


@router.get("/logs", response_model=LogListResponse)
async def list_logs(limit: int = Query(100, ge=1, le=1000)):
    try:
        logs = await get_logs(limit=limit)
        return LogListResponse(
            logs=LogCategoryResponse(
                errors=[LogEntry(log=log) for log in logs["errors"]],
                info=[LogEntry(log=log) for log in logs["info"]],
            )
        )
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessages.LOG_RETRIEVAL_ERROR)
