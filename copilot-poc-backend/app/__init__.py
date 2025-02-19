from flask import Flask
from flask_cors import CORS
from config import Config
from app.db import db
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # Enable CORS for frontend requests
    db.init_app(app)

    # Register blueprints (modular routing)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(routes_bp, url_prefix="/api")

    return app
