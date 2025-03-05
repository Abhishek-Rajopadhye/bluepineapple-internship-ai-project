from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.call_service import generate_jitsi_link

# FastAPI router
router = APIRouter()

@router.get("/call-technician")
async def call_technician():
    """
    Returns a Jitsi Meet link for initiating a VoIP call.
    """
    jitsi_url = generate_jitsi_link()
    return JSONResponse(content={"jitsi_url": jitsi_url}, status_code=200)