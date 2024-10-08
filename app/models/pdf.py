from pydantic import BaseModel, Field
from typing import List


class PDFResponse(BaseModel):
    pdf_id: str = Field(..., description="Unique identifier for the uploaded PDF")


class ChatRequest(BaseModel):
    message: str = Field(
        ..., min_length=1, max_length=1000, description="User's message for the chat"
    )


class ChatResponse(BaseModel):
    response: str = Field(
        ..., description="AI-generated response to the user's message"
    )


class PDFListItem(BaseModel):
    id: str = Field(..., alias="_id", description="Unique identifier for the PDF")
    filename: str = Field(..., description="Name of the PDF file")

    class Config:
        populate_by_name = True


class PDFListResponse(BaseModel):
    pdfs: List[PDFListItem] = Field(
        ..., description="List of PDFs stored in the system"
    )


class LogEntry(BaseModel):
    log: str = Field(..., description="Formatted log entry")


class LogCategoryResponse(BaseModel):
    errors: List[LogEntry] = Field(..., description="List of error log entries")
    info: List[LogEntry] = Field(..., description="List of info log entries")


class LogListResponse(BaseModel):
    logs: LogCategoryResponse = Field(..., description="Categorized log entries")
