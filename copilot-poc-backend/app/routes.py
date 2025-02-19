from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from twilio.rest import Client
import openai

routes_bp = Blueprint("routes", __name__)

openai.api_key = "your-openai-api-key"

@routes_bp.route("/copilot", methods=["POST"])
@jwt_required()
def copilot_chat():
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