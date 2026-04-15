import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
print("Key length:", len(GEMINI_API_KEY))

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

print("Testing Gemini via OpenAI compatibility...")
try:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": "Return JSON: {'hello': 'world'}."}],
        response_format={"type": "json_object"}
    )
    print(response.choices[0].message.content)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
