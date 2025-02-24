from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.db import db
from app.auth import auth_bp
from app.routes import routes_bp

def create_app():
    """
    Create and configure the Flask application.
    This function initializes the Flask app, configures it using the settings
    from the Config object, enables Cross-Origin Resource Sharing (CORS) for
    frontend requests, initializes the database with the app context, and
    registers the authentication and main route blueprints.
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # Enable CORS for frontend requests
    db.init_app(app)

    # Register blueprints (modular routing)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(routes_bp, url_prefix="/api")

    return app
