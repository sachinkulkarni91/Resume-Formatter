import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
print("Listing models...")
try:
    response = requests.get(url)
    models = response.json()
    for m in models.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print(m["name"])
except Exception as e:
    print(e)
