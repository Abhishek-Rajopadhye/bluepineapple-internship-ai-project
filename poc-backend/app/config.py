import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

class Config:
    """
    Configuration class for the FastAPI application.
    Loads environment variables and provides default values where necessary.
    """

    # General Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///poc.db")

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Hugging Face LLM API Configuration
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL_URL = os.getenv(
        "HUGGINGFACE_MODEL_URL",
        "https://api-inference.huggingface.co/models/meta-llama/llama-3.3-70b-instruct"
    )
