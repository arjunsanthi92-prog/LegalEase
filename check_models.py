import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY is missing")
    exit()

client = genai.Client(api_key=api_key)

print("\nGemini models available for this API key:\n")

try:
    for model in client.models.list():
        if "generateContent" in model.supported_actions:
            print(model.name)

except Exception as error:
    print("\nCould not connect to Gemini.")
    print(error)