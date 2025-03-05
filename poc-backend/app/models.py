from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from app.db import Base

class User(Base):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The unique username for the user.
        password_hash (str): The hashed password for the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)


class Conversation(Base):
    """
    Represents a conversation in the application.

    Attributes:
        id (int): The unique identifier for the conversation.
        user_id (int): The user ID associated with the conversation.
        messages (JSON): The conversation history stored as JSON.
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    messages = Column(JSON, nullable=False)

