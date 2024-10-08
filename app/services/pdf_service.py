import PyPDF2
from fastapi import UploadFile
from app.core.logging import logger
from app.database.pdf_storage import store_pdf_content
from io import BytesIO


async def process_pdf(file: UploadFile, pdf_id: str, filename: str):
    content = await file.read()
    pdf_reader = PyPDF2.PdfReader(BytesIO(content))

    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()

    await store_pdf_content(pdf_id, extracted_text, filename)
    logger.info(f"Processed and stored PDF with ID: {pdf_id}")

    return extracted_text
