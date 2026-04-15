import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{"parts": [{"text": "Hello, return JSON with key 'status' and value 'ok'"}]}],
    "generationConfig": {"responseMimeType": "application/json"}
}

try:
    print("Sending request to Gemini API...")
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status: {response.status_code}")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
