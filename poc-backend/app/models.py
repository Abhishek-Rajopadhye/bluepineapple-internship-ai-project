from app.db import db

class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The unique username for the user.
        password_hash (str): The hashed password for the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


class Conversation(db.Model):
    """
    Represents a conversation in the application.

    Attributes:
        id (int): The unique identifier for the conversation.
        user_id (str): The unique id foreign key of the user.
        messages (JSON): The messages of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    messages = db.Column(db.JSON, nullable=False)

    def __init__(self, user_id, messages):
        self.user_id = user_id
        self.messages = messages