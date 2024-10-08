import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.pdf_service import process_pdf
from app.models.pdf import PDFResponse, PDFListResponse, PDFListItem
from app.database.pdf_storage import get_all_pdfs
from app.core.error_messages import ErrorMessages
from app.core.logging import logger

router = APIRouter()


@router.post("/pdf", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=ErrorMessages.INVALID_FILE_TYPE)

    pdf_id = str(uuid.uuid4())

    try:
        await process_pdf(file, pdf_id, file.filename)
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessages.PDF_PROCESSING_ERROR)

    return PDFResponse(pdf_id=pdf_id)


@router.get("/get_pdfs", response_model=PDFListResponse)
async def list_pdfs(limit: int = Query(100, ge=1, le=1000)):
    try:
        pdfs = await get_all_pdfs(limit=limit)
        return PDFListResponse(
            pdfs=[PDFListItem(id=pdf["_id"], filename=pdf["filename"]) for pdf in pdfs]
        )
    except Exception as e:
        logger.error(f"Error retrieving PDFs: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessages.DATABASE_ERROR)
