import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
MODEL_NAME = os.getenv("MODEL_NAME")

# Check if the API key is set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

if not MODEL_NAME:
    raise ValueError("MODEL_NAME not found. Please set it in your .env file.")
