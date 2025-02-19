import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the application.
    Attributes:
        SECRET_KEY (str): Secret key for the application, default is "supersecretkey".
        DATABASE_URL (str): URL for the database connection, default is "sqlite:///./copilot_poc.db".
        JWT_SECRET_KEY (str): Secret key for JWT, default is "jwtsecretkey".
        TWILIO_ACCOUNT_SID (str): Account SID for Twilio, fetched from environment variable.
        TWILIO_AUTH_TOKEN (str): Authentication token for Twilio, fetched from environment variable.
        TWILIO_PHONE_NUMBER (str): Phone number for Twilio, fetched from environment variable.
        OPENAI_API_KEY (str): API key for OpenAI, fetched from environment variable.
    """
    
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_URL = "sqlite:///./copilot_poc.db"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_SECREY_KEY")
