from fastapi import FastAPI, Depends, HTTPException, Header, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import logging
import sys
from .rag import process_simple_request

from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import uuid

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

# SQLite database setup
DATABASE_URL = "sqlite:///./chat_history.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    thread_id = Column(String)
    sequence_id = Column(Integer)
    user_message = Column(Text)
    assistant_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basic verification function to authorize requests
async def verify_request(authorization: Optional[str] = Header(None)):
    api_key = os.environ.get("API_KEY")
    if not authorization or authorization != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/health")
async def health():
    return {"status": "ok"}

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

        db = SessionLocal()
        
        # Retrieve conversation history
        chat_history = db.query(ChatMessage).filter(ChatMessage.thread_id == threadId).order_by(ChatMessage.sequence_id).all()

        # Format history for OpenAI
        messages = []
        for msg in chat_history:
            messages.append({"role": "user", "content": msg.user_message})
            messages.append({"role": "assistant", "content": msg.assistant_message})
        
        # Add new user message
        messages.append({"role": "user", "content": message})
        
        # Generate response with full history
        response = process_simple_request(chat_history=messages)
        
        # Store both messages in one entry
        db.add(ChatMessage(
            id=conversationId,
            thread_id=threadId,
            sequence_id=int(sequenceId),
            user_message=message,
            assistant_message=response
        ))
        db.commit()

        return {"message": response}
    except Exception as e:
        db.rollback()
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()