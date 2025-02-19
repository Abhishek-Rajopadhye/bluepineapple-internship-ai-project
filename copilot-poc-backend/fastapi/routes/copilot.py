from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
import openai
from config import Config
from database import get_db
from models import Conversation

router = APIRouter()
openai.api_key = Config.OPENAI_API_KEY

@router.post("/copilot")
def copilot_chat(message: str, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Handles a chat message from the user, generates a response using OpenAI's GPT-4 model, 
    and stores the conversation in the database.
    Args:
        message (str): The message from the user.
        Authorize (AuthJWT, optional): Dependency for JWT authorization. Defaults to Depends().
        db (Session, optional): Dependency for the database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: If no message is provided, raises a 400 HTTP exception.
    Returns:
        dict: A dictionary containing the AI's reply to the user's message.
    """
    
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()

    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    ai_reply = response["choices"][0]["message"]["content"]

    conversation = Conversation(user_id=user_id, message=message, response=ai_reply)
    db.add(conversation)
    db.commit()

    return {"reply": ai_reply}
