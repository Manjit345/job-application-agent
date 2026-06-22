"""
Utils: Shared utility function used across all agent tools.
Implements retry logic with exponential backoff for Gemini API calls to handle temporary service unavailability gracefully.
"""

import time
import os
from dotenv import load_dotenv
from google import genai

def call_with_retry(client, model: str, contents: str, config: dict, max_retries: int = 3):
    """
    Call the model's API with automatic retry on 503 Unavailable errors.

    Args:
        client: The model's client object
        model: The name of the model
        contents: Prompt text to send to the model.
        config: Generation config dictionary.
        max_retries: Maximum number of retry attempts before giving up

    Returns:
        The model's API response object

    Raises:
        If all retries are exhausted or a non 503 error occurs.
    """
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
            raise e
    raise Exception("The model's API is unavailable after multiple retries")

#Code for unit testing the function
if __name__ == "__main__":
    load_dotenv()

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    response = call_with_retry(
        client=client,
        model="gemini-3.5-flash",
        contents="Say hello in one sentence.",
        config={"response_mime_type": "text/plain"}
    )

    print(response.text)