import os

class Config:
    """
    Configuration class for the application.
    Attributes:
        SECRET_KEY (str): Secret key for the application, default is 'supersecretkey'.
        SQLALCHEMY_DATABASE_URI (str): URI for the SQLAlchemy database, default is 'sqlite:///copilot_poc.db'.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to track modifications in SQLAlchemy, default is False.
        JWT_SECRET_KEY (str): Secret key for JWT, default is 'jwtsecretkey'.
        TWILIO_ACCOUNT_SID (str): Account SID for Twilio, fetched from environment variable.
        TWILIO_AUTH_TOKEN (str): Auth token for Twilio, fetched from environment variable.
        TWILIO_PHONE_NUMBER (str): Phone number for Twilio, fetched from environment variable.
    """
    
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///copilot_poc.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")

    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
