import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
print("Key length:", len(GEMINI_API_KEY))

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("Testing connection...")
    response = model.generate_content('Hello! Give me a valid JSON object with {"key": "value"}',
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json"
        ))
    print("Response payload:")
    print(response.text)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
