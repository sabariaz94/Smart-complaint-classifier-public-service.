import json
import os
import uuid
from datetime import datetime
import pandas as pd

# Define the absolute path for the data directory and the complaints file
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "database")
COMPLAINTS_FILE = os.path.join(DATA_DIR, "complaints.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_complaints() -> list:
    """
    Loads all complaints from the JSON file.
    Returns an empty list if the file doesn't exist or is empty/invalid.
    """
    if not os.path.exists(COMPLAINTS_FILE):
        return []
    try:
        with open(COMPLAINTS_FILE, "r", encoding="utf-8") as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading complaints: {e}")
        return []

def save_complaints(complaints: list):
    """Saves the entire list of complaints to the JSON file."""
    try:
        with open(COMPLAINTS_FILE, "w", encoding="utf-8") as f:
            json.dump(complaints, f, indent=4)
    except IOError as e:
        print(f"Error saving complaints: {e}")

def save_complaint(complaint_data: dict) -> dict:
    """
    Adds a single new complaint to the database.
    This is more efficient than reading and writing the whole file.
    """
    all_complaints = load_complaints()
    
    # Create the full complaint record
    new_complaint = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "status": "New",
        "notes": [],
        **complaint_data, # Merge classified data
    }
    
    all_complaints.append(new_complaint)
    save_complaints(all_complaints)
    
    return new_complaint

def update_complaint_status(complaint_id: str, status: str, note: str):
    """Updates the status and adds a note to a specific complaint."""
    complaints = load_complaints()
    updated = False
    for complaint in complaints:
        if complaint.get("id") == complaint_id:
            complaint["status"] = status
            if note:
                # Ensure 'notes' key exists and is a list
                if "notes" not in complaint or not isinstance(complaint["notes"], list):
                    complaint["notes"] = []
                
                complaint["notes"].append(
                    {"timestamp": datetime.now().isoformat(), "note": note}
                )
            updated = True
            break
            
    if updated:
        save_complaints(complaints)

def search_complaints(query: str) -> list:
    """
    Searches complaints by keyword in summary, keywords, or full text.
    The search is case-insensitive.
    """
    complaints = load_complaints()
    if not query:
        return complaints # Return all if query is empty
        
    query = query.lower()
    results = []
    
    for complaint in complaints:
        # Ensure all fields are strings before calling .lower()
        summary = str(complaint.get("summary", "")).lower()
        complaint_text = str(complaint.get("complaint_text", "")).lower()
        
        # Handle keywords, which is a list
        keywords = [str(k).lower() for k in complaint.get("keywords", [])]
        keyword_str = " ".join(keywords)

        if query in summary or query in complaint_text or query in keyword_str:
            results.append(complaint)
            
    return results

def export_to_csv(filename: str) -> bool:
    """Exports all complaints to a CSV file."""
    complaints = load_complaints()
    if not complaints:
        return False
    
    try:
        df = pd.DataFrame(complaints)
        
        # Safely handle list-to-string conversion for 'keywords' and 'notes'
        if 'keywords' in df.columns:
            df['keywords'] = df['keywords'].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else "")
        if 'notes' in df.columns:
            df['notes'] = df['notes'].apply(lambda x: str(x) if x else "")

        df.to_csv(filename, index=False, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def export_to_json(filename: str) -> bool:
    """Exports all complaints to a JSON file."""
    complaints = load_complaints()
    if not complaints:
        return False
        
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(complaints, f, indent=4)
        return True
    except IOError as e:
        print(f"Error exporting to JSON: {e}")
        return False