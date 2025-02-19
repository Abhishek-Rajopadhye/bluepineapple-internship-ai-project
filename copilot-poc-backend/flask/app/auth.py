from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from app.db import db

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

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

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.

    This endpoint handles the registration of a new user by accepting a JSON payload
    with a username and password. The password is hashed before being stored in the database.

    Request JSON format:
        {
            "username": "user's username",
            "password": "user's password"
        }

    Returns:
        JSON response with a success message and HTTP status code 201 if the registration is successful.
    """
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and generates an access token.
    This function retrieves JSON data from the request, checks the user's credentials,
    and if valid, generates an access token for the user.
    Returns:
        Response: A JSON response containing the access token and a status code of 200 if
                  authentication is successful.
        Response: A JSON response containing an error message and a status code of 401 if
                  authentication fails.
    """
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
