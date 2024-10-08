import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from app.database.pdf_storage import get_pdf_content

genai.configure(api_key=settings.GEMINI_API_KEY)


async def generate_response(pdf_id: str, user_message: str):
    pdf_content = await get_pdf_content(pdf_id)
    if not pdf_content:
        raise ValueError(f"PDF content not found for ID: {pdf_id}")

    prompt = f"PDF Content: {pdf_content}\n\nUser Question: {user_message}\n\nAnswer:"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    logger.info(f"Generated response for PDF ID: {pdf_id}")

    return response.text
