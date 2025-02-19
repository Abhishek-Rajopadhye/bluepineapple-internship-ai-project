from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from twilio.rest import Client
from config import Config

router = APIRouter()
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

@router.post("/call-technician")
def call_technician(phone: str, Authorize: AuthJWT = Depends()):
    """
    Initiates a call to a technician using the provided phone number.
    Args:
        phone (str): The phone number to call.
        Authorize (AuthJWT, optional): Dependency that ensures the user is authorized via JWT.
    Raises:
        HTTPException: If the phone number is not provided or if there is an issue with the call.
    Returns:
        dict: A dictionary containing a message indicating the call was initiated and the call SID.
    """
    
    Authorize.jwt_required()
    
    if not phone:
        raise HTTPException(status_code=400, detail="Phone number required")

    call = twilio_client.calls.create(
        to=phone,
        from_=Config.TWILIO_PHONE_NUMBER,
        twiml="<Response><Say>Connecting you to a technician.</Say></Response>"
    )

    return {"message": "Call initiated", "call_sid": call.sid}
