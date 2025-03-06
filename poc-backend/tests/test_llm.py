import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_llm_chat(client):
    """
    Test sending a chat message to the LLM API.

    Registers a user, logs in, and sends a message to the LLM.

    Parameters:
        client (AsyncClient): The test HTTP client.

    Asserts:
        - The response status code is 200 (OK).
        - The response contains a valid reply from the LLM.
    """
    await client.post("/api/auth/register", json={"emailId": "testuser@example.com", "password": "testpass"})
    
    # Login user and print response for debugging
    login_response = await client.post("/api/auth/login", json={"emailId": "testuser@example.com", "password": "testpass"})
    
    assert login_response.status_code == 200, "Login request failed"
    assert "access_token" in login_response.json(), "Login response does not contain access_token"

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    with patch("app.services.llm_service.query_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Hello, how can I help you?"
        response = await client.post("/api/llm/", json={"message": "Hello"}, headers=headers)

    assert response.status_code == 200
    assert response.json()["reply"] == "Hello, how can I help you?"
