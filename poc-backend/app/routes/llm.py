from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models import Conversation
from app.dependencies import get_current_user
from app.services.llm_service import query_llm
from pydantic import BaseModel
from typing import List, Dict

# FastAPI router
router = APIRouter()

# Pydantic model for request validation
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def llm_chat(request: ChatRequest, 
                   db: AsyncSession = Depends(get_db), 
                   current_user=Depends(get_current_user)):
    """
    Handle chat requests to the LLM AI model.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Retrieve conversation history
    result = await db.execute(select(Conversation).where(Conversation.user_id == current_user.id))
    conversation = result.scalars().first()
    conversation_history: List[Dict[str, str]] = conversation.messages if conversation else []

    # Append user message to history
    conversation_history.append({"role": "user", "content": request.message})

    # Query LLM via Hugging Face
    reply = await query_llm(conversation_history)

    # Append AI response to history
    conversation_history.append({"role": "llm", "content": reply})

    # Update or create conversation in the database
    if conversation:
        conversation.messages = conversation_history
    else:
        new_conversation = Conversation(user_id=current_user.id, messages=conversation_history)
        db.add(new_conversation)
    await db.commit()

    return {"reply": reply}
