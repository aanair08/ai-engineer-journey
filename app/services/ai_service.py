import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"


def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:")
    print(response.text)

    # Handle empty response
    if not response.text:
        return "Empty API response"

    try:
        response_json = response.json()
    except Exception as e:
        return f"Invalid JSON response: {str(e)}"

    if "choices" not in response_json:
        return f"Unexpected API response: {response_json}"

    return response_json["choices"][0]["message"]["content"]