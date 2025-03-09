from fastapi import FastAPI, Depends, HTTPException, Header, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import logging
import sys
# from .rag import process_rag_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Basic verification function to authorize requests
async def verify_request(authorization: Optional[str] = Header(None)):
    api_key = os.environ.get("API_KEY")
    logging.info(f"Authorization header received: {authorization}")
    if not authorization or authorization != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.post("/api/chat")
async def chat(
    message: str = Form(...),
    conversationId: str = Form(...),
    threadId: str = Form(...),
    sequenceId: str = Form(...),
    file: Optional[UploadFile] = File(None),
    authorized: bool = Depends(verify_request)
):
    try:
        # Process the file if needed (later)
        if file:
            file_content = await file.read()
            logging.info(f"Received file: {file.filename}")
            logging.info(f"File content: {file_content[:100]}")

        # response = process_rag_request(
        #     query=message,
        #     collection_name=None,
        #     additional_context=None
        # )
        # return {"response": response}
        response = f"Message received: '{message}'. AI Chat is coming soon.."

        logging.info(f"Received message: {message} {threadId} {conversationId} {sequenceId}")
        return {"message": response}
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 9000)))