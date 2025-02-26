from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from twilio.rest import Client
from app.db import db
from app.models import Conversation
import openai
import os

routes_bp = Blueprint("routes", __name__)

api_key = os.getenv("OPENROUTER_API_KEY")
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

@jwt_required
@routes_bp.route("/llm", methods=["POST"])
def llm_chat():
    """
    Endpoint to handle chat requests to the LLM AI model.
    This endpoint expects a POST request with a JSON payload containing a "message" field.
    It uses the llm model to generate a response based on the user's message.
    Returns the reply on successful generation else raises error.
    Returns:
        JSON response containing the AI-generated reply or an error message.
    Raises:
        400 : Bad Request. If no message is provided in the request.
        500 : Internal Server Error. If there is an issue with the OpenAI API call or other exceptions.
    Models:
        deepseek/deepseek-r1-distill-llama-70b:free
        deepseek/deepseek-r1:free
        cognitivecomputations/dolphin3.0-r1-mistral-24b:free
        google/gemini-2.0-pro-exp-02-05:free
        meta-llama/llama-3.3-70b-instruct:free
    """
    data = request.json
    user_message = data.get("message", "")
    user_id = data.get("user_id", -1)

    if(user_message == ""):
        return jsonify({"error": str(exception)}), 400

    # Retrieve conversation history from the database
    conversation = Conversation.query.filter_by(user_id=user_id).first()
    if conversation:
        conversation_history = conversation.messages
    else:
        conversation_history = []

    # Add the new user message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    try:
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=conversation_history
        )
        reply = chat_completion.choices[0].message.content

        # Add the AI's reply to the conversation history
        conversation_history.append({"role": "llm", "content": reply})

        # Save the updated conversation history in the database
        if conversation:
            conversation.messages = conversation_history
        else:
            new_conversation = Conversation(user_id=user_id, messages=conversation_history)
            db.session.add(new_conversation)
        db.session.commit()

        return jsonify({"reply": reply})
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500

@jwt_required
@routes_bp.route("/call-technician", methods=["POST"])
def call_technician():
    """
    Initiates a call to a technician using the Twilio API.
    This function retrieves the customer's phone number from the JSON request data,
    validates it, and then uses the Twilio API to initiate a call to the provided number.
    The call will play a message indicating that the customer is being connected to a technician.
    
    Returns:
        A JSON response indicating the result of the call initiation. If the call is successfully initiated, returns a success message with the call SID.
    Raises:
        500, KeyError: If the required Twilio configuration keys are not found in the current app config.
        500, Exception: If there is an issue with the Twilio API call or other exceptions.
    """
    try:
        data = request.json
        customer_phone = data.get("phone") if data else "+919767724238"

        client = Client(current_app.config["TWILIO_ACCOUNT_SID"], current_app.config["TWILIO_AUTH_TOKEN"])
        call = client.calls.create(
            to=customer_phone,
            from_=current_app.config["TWILIO_PHONE_NUMBER"],
            twiml="<Response><Say>Connecting you to a technician.</Say></Response>"
        )
        return jsonify({"message": "Call initiated", "call_sid": call.sid}), 200
    except KeyError:
        return jsonify({"error": "Twilio configuration missing"}), 500
    except Exception as exception:
        return jsonify({"error": str(exception)}), 500
