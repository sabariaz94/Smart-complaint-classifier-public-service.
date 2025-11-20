import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

print("\n=== AVAILABLE MODELS IN YOUR ACCOUNT ===\n")
for m in genai.list_models():
    print(m.name)
