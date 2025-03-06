from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.call_service import generate_jitsi_link

# FastAPI router
router = APIRouter()

@router.get("/call-technician")
async def call_technician():
    """
    Returns a Jitsi Meet link for initiating a VoIP call.

    Returns:
        JSONResponse: A JSON response containing the Jitsi Meet link.

    Raises:
        HTTPException: If there is an error generating the Jitsi Meet link.
    """
    try:
        jitsi_url = generate_jitsi_link()
        return JSONResponse(content={"jitsi_url": jitsi_url}, status_code=200)
    except Exception as callError:
        print(f"Error generating Jitsi Meet link: {callError}")
        raise HTTPException(status_code=500, detail="Internal server error")