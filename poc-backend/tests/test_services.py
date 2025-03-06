import pytest
from app.services.call_service import generate_jitsi_link
from app.services.llm_service import query_llm
from unittest.mock import AsyncMock, patch

def test_generate_jitsi_link():
    """
    Test Jitsi Meet link generation.

    Asserts:
        - The generated link starts with "https://meet.jit.si/".
    """
    url = generate_jitsi_link()
    assert url.startswith("https://meet.jit.si/")

@pytest.mark.asyncio
async def test_query_llm():
    """
    Test the LLM service function.

    Uses a mock API response to test `query_llm`.

    Asserts:
        - The function correctly returns the mock AI response.
    """
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json.return_value = [{"generated_text": "Hello! How can I help you today?"}]
        response = await query_llm([{"role": "user", "content": "Hello. Please say Hello! How can I help you today?"}])

    assert response == "Hello! How can I help you today?"