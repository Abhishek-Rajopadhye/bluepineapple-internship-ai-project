import httpx
import os
from app.config import Config
from huggingface_hub import InferenceClient
from httpx import HTTPStatusError

HUGGINGFACE_API_URL = Config.HUGGINGFACE_MODEL_URL
HUGGINGFACE_API_KEY = Config.HUGGINGFACE_API_KEY

async def query_llm(conversation_history):
    """
    Send a conversation history to Hugging Face API and retrieve a response.

    Parameters:
        conversation_history (list): A list of dictionaries representing the conversation history.

    Returns:
        str: The response from the LLM.

    Raises:
        HTTPStatusError: If there is an error with the HTTP request.
        Exception: If there is any other error.
    """
    huggingfaceClient = InferenceClient(
        provider="fireworks-ai",
        api_key=HUGGINGFACE_API_KEY
    )

    try:
        async with httpx.AsyncClient() as client:
            completion = huggingfaceClient.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct",
                messages=conversation_history,
            )
            data = completion.choices[0].message
            return data.content if data else "No response from LLM"
    except HTTPStatusError as http_error:
        print(f"HTTP error occurred: {http_error}")
        raise
    except Exception as error:
        print(f"An error occurred: {error}")
        raise
