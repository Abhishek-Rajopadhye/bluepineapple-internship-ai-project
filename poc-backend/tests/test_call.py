import pytest
from unittest.mock import patch
from app.services.call_service import generate_jitsi_link

@pytest.mark.asyncio
async def test_call_technician(client):
    """
    Test the call-technician API.

    Calls the API to generate a Jitsi Meet link and verifies the response.

    Parameters:
        client (AsyncClient): The test HTTP client.

    Asserts:
        - The response status code is 200 (OK).
        - The response contains a valid Jitsi Meet link.
    """
    response = await client.get("/api/call/call-technician")
    assert response.status_code == 200
    assert "jitsi_url" in response.json()
    assert response.json()["jitsi_url"].startswith("https://meet.jit.si/")
