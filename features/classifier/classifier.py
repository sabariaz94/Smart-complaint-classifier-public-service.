import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY, MODEL_NAME

# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

# Use the model name from the config
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Error creating GenerativeModel: {e}")
    # Handle the error appropriately, maybe by exiting or using a fallback.
    # For now, we'll raise it to make it visible during development.
    raise

def classify_complaint(complaint_text: str) -> dict:
    """
    Classifies a public complaint using the Gemini API.

    Args:
        complaint_text: The complaint text to classify.

    Returns:
        A dictionary with classification details or an error message.
    """
    if not complaint_text:
        return {
            "error": "Complaint text cannot be empty.",
            "category": "Other",
            "priority": "Low",
        }

    prompt = f"""
    Analyze the following public service complaint and provide a structured JSON output.

    **Complaint:**
    "{complaint_text}"

    **Instructions:**
    1.  **Categorize** the complaint into ONE of the following: `Electricity`, `Water`, `Roads`, `Waste`, `Health`, `Security`, `Other`.
    2.  **Determine the Priority Level:** `High`, `Medium`, or `Low`.
    3.  **Create a concise one-sentence summary** of the core issue.
    4.  **Extract key terms** as a list of strings.
    5.  **Provide a confidence score** (0.0 to 1.0) for the classification.

    **Return a single, clean JSON object with no markdown or extra text.**
    **JSON Format:**
    {{
      "category": "...",
      "priority": "...",
      "summary": "...",
      "keywords": ["...", "..."],
      "confidence": ...
    }}
    """

    try:
        response = model.generate_content(prompt)
        
        # Enhanced parsing to handle potential markdown and variations
        raw_text = response.text.strip()
        
        # Use regex to find the JSON block, which is more robust
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if not json_match:
            print(f"Error: No JSON object found in the response from the model. Raw response: {raw_text}")
            return {"error": "Failed to parse model's response."}
            
        json_str = json_match.group(0)
        
        # Attempt to parse the extracted JSON string
        classification = json.loads(json_str)
        
        # Add the original complaint text to the result
        classification['complaint_text'] = complaint_text
        
        return classification

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from model response: {e}")
        print(f"Raw response part for debugging: {json_str}")
        return {"error": "JSON decoding failed.", "raw_response": raw_text}
    except Exception as e:
        print(f"An unexpected error occurred during classification: {e}")
        print(f"Raw response: {response.text if 'response' in locals() else 'N/A'}")
        return {"error": f"An unexpected error occurred: {e}"}


# ----------------- Test Example -----------------
if __name__ == "__main__":
    test_complaint = (
        "The streetlights in my neighborhood have been out for a week. "
        "It's very dark and feels unsafe at night. I'm worried about crime."
    )

    result = classify_complaint(test_complaint)

    if result and "error" not in result:
        print("Classification successful:")
        print(json.dumps(result, indent=4))
    else:
        print("Classification failed.")
        if result:
            print("Reason:", result.get("error"))

