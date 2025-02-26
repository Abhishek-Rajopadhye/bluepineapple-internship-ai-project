from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.db import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

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
    Raises:
        500: Internal Server Error. If any error occurs during registration.
    """
    try:
        data = request.json
        hashed_password = generate_password_hash(data["password"]).decode("utf-8")
        user = User(username=data["emailId"], password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and generates an access token.
    This function retrieves JSON data from the request, checks the user's credentials,
    and if valid, generates an access token for the user.
    Returns:
        A JSON response containing the access token and a status code of 200 if authentication is successful.
    Raises:
        401: Invalid Credentials
        500: Internal Server Error. If there is any error duringh login.
    """
    try:
        data = request.json
        user = User.query.filter_by(username=data["emailId"]).first()
        if user and check_password_hash(user.password_hash, data["password"]):
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token, "user_id": user.id}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as exception:
        return jsonify({"error": "Internal Error" + str(exception)}), 500