from fastapi import APIRouter, HTTPException
from app.services.llm_service import generate_response
from app.models.pdf import ChatRequest, ChatResponse
from app.core.error_messages import ErrorMessages
from app.core.logging import logger

router = APIRouter()


@router.post("/chat/{pdf_id}", response_model=ChatResponse)
async def chat_with_pdf(pdf_id: str, request: ChatRequest):
    try:
        response = await generate_response(pdf_id, request.message)
        return ChatResponse(response=response)
    except ValueError as e:
        logger.error(f"PDF not found: {str(e)}")
        raise HTTPException(status_code=404, detail=ErrorMessages.PDF_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessages.CHAT_RESPONSE_ERROR)
