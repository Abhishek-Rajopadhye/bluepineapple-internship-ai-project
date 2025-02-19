from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from twilio.rest import Client
import openai
import os

routes_bp = Blueprint("routes", __name__)

openai.api_key = os.getenv("OPENAI_API_SECRET_KEY")

@routes_bp.route("/copilot", methods=["POST"])
@jwt_required()
def copilot_chat():
    """
    Endpoint to handle chat requests to the Copilot AI model.
    This endpoint expects a POST request with a JSON payload containing a "message" field.
    It uses the OpenAI GPT-4 model to generate a response based on the user's message.
    Returns:
        JSON response containing the AI-generated reply or an error message.
    Raises:
        400 Bad Request: If no message is provided in the request.
        500 Internal Server Error: If there is an issue with the OpenAI API call or other exceptions.
    """
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": response["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_bp.route("/call-technician", methods=["POST"])
@jwt_required()
def call_technician():
    """
    Initiates a call to a technician using the Twilio API.
    This function retrieves the customer's phone number from the JSON request data,
    validates it, and then uses the Twilio API to initiate a call to the provided number.
    The call will play a message indicating that the customer is being connected to a technician.
    Returns:
        Response: A JSON response indicating the result of the call initiation.
                  If the phone number is not provided, returns an error message with a 400 status code.
                  If the call is successfully initiated, returns a success message with the call SID.
    Raises:
        KeyError: If the required Twilio configuration keys are not found in the current app config.
    """
    
    data = request.json
    customer_phone = data.get("phone")

    if not customer_phone:
        return jsonify({"error": "Phone number required"}), 400

    client = Client(current_app.config["TWILIO_ACCOUNT_SID"], current_app.config["TWILIO_AUTH_TOKEN"])
    call = client.calls.create(
        to=customer_phone,
        from_=current_app.config["TWILIO_PHONE_NUMBER"],
        twiml="<Response><Say>Connecting you to a technician.</Say></Response>"
    )

    return jsonify({"message": "Call initiated", "call_sid": call.sid})