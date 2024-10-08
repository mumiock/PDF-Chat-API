# PDF Chat API

## Overview

This project is a FastAPI application that allows users to upload PDF files and interact with them through a chat interface. It uses Google's Gemini AI model for generating responses and MongoDB for data storage.

## Features

- PDF upload and storage
- Chat interface for interacting with uploaded PDFs
- Logging system with MongoDB storage
- API endpoints for PDF management, chat, and log retrieval

## Setup Instructions

1. Clone the repository.
2. Create a `.env` file in the root directory with the following settings:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   MONGODB_URL=your_mongodb_url
   MONGODB_DB_NAME=your_database_name
   ```
3. Install dependencies using `pip install -r requirements.txt`.
4. Run the application using `uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload`.

## API Endpoints

### PDF Management

- **Upload PDF**
  - Method: POST
  - Endpoint: `/v1/pdf`
  - Description: Upload a PDF file.
  - Response: JSON with the PDF ID.

- **List PDFs**
  - Method: GET
  - Endpoint: `/v1/get_pdfs`
  - Description: Retrieve a list of uploaded PDFs.
  - Query Parameters: `limit` (optional, default: 100)

### Chat

- **Chat with PDF**
  - Method: POST
  - Endpoint: `/v1/chat/{pdf_id}`
  - Description: Interact with a specific PDF.
  - Request Body: JSON with a `message` field.
  - Response: JSON with the AI-generated answer.

### Logs

- **Retrieve Logs**
  - Method: GET
  - Endpoint: `/v1/logs`
  - Description: Retrieve application logs.
  - Query Parameters: `limit` (optional, default: 100)

## Deployment

To deploy the application using Docker:

1. Ensure Docker is installed on your system.
2. Build the Docker image:
   ```
   docker build -t pdf-chat-api .
   ```
3. Run the container:
   ```
   docker run -p 8000:8000 -e GEMINI_API_KEY=your_key -e MONGODB_URL=your_url -e MONGODB_DB_NAME=your_db pdf-chat-api
   ```

The API will be available at `http://localhost:8000`.

## Project Structure

- `app/`: Main application directory
  - `api/`: API route handlers
  - `core/`: Core configurations and utilities
  - `database/`: Database connection and operations
  - `models/`: Pydantic models for request/response
  - `services/`: Business logic and external service integrations
- `tests/`: Test files
- `Dockerfile`: Docker configuration for deployment
- `requirements.txt`: Python dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
