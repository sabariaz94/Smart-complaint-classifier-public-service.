Smart Complaint Classifier for Public Services (CLI Project)
Project Overview

A professional CLI application that classifies public-service complaints (e.g., electricity, water, roads, waste management) using an AI model (Gemini).
The system helps government/public-service teams automatically categorize complaints and store them for further processing.

Core Features

Complaint submission via CLI

AI-powered complaint classification (Gemini API)

Multi-class categories (Electricity, Water, Roads, Waste, Health, Security, Other)

Priority detection (High/Medium/Low)

Complaint history storage

Search & filter complaints

CSV/JSON export for government use

Optional simple Streamlit dashboard (complaint trends & stats)

Tech Stack

Language: Python 3.11+

CLI Framework: Questionary (interactive menu)

UI Library: Rich (tables, panels, alerts)

AI Model: Gemini API (text classification)

Storage: Plain text files or JSON storage

Package Manager: UV

Project Structure
smart-complaint-classifier/
├── main.py                        # Entry point & menu loop
├── config.py                      # Gemini API setup
├── database/
│   └── complaints.json            # All stored complaints
└── features/
    ├── classifier/
    │   ├── GEMINI.md             # Prompt design for classification
    │   └── classifier.py          # Calls Gemini API
    ├── complaints/
    │   ├── GEMINI.md
    │   └── complaints.py         # CRUD operations on complaints
    ├── analytics/
    │   ├── GEMINI.md
    │   └── analytics.py          # Stats, trending issues

AI Classification Rules (Gemini Prompt Guidelines)

Your classifier should extract:

Category: Electricity / Water / Roads / Waste / Health / Security / Other

Priority: High / Medium / Low

Summary: Short 1–2 sentence summary

Keywords: Important words from complaint

Confidence Score

Example Gemini Response Format
{
  "category": "Water",
  "priority": "High",
  "summary": "Water pipeline is broken near the main street causing heavy leakage.",
  "keywords": ["pipeline", "water leakage"],
  "confidence": 0.92
}

Complaint Categories

Electricity

Water

Roads

Waste Management

Health

Public Safety & Security

Other

CLI Interaction

Your CLI uses:

Questionary for menu & selections

Rich for colourful tables & panels

Example Menu

1. File a Complaint
2. View All Complaints
3. Search Complaints
4. Export Data
5. Analytics Dashboard
6. Exit
# Gemini Fix Prompt

I am sharing a Python Streamlit project. It has multiple problems:

1. Gemini API errors (model not found, wrong model name, incorrect client usage).
2. Complaints are not being saved, so View Complaints, Search Complaints, and Analytics pages show nothing.
3. File paths for saving and loading complaints may be incorrect.
4. I want all complaints to be saved in a JSON file or database and displayed correctly in all pages.
5. I want you to automatically inspect all project files and fix every error.

Below is the full project folder. Analyze all Python files and then do the following:

## REQUIRED FIXES

1. Correct the Google Generative AI API usage for Python using the latest supported model.
2. Replace deprecated model names (such as `gemini-1.5-flash` / `gemini-1.5-flash-001`) with a valid model discovered via `ListModels` automatically.
3. Fix `classify_complaint()` so it works with the correct API pattern and robustly handles JSON output.
4. Make sure complaints are saved permanently to a file (for example: `data/complaints.json`).
5. Create save and load functions:

   * `save_complaint(data)`
   * `load_complaints()`
6. Ensure the File a Complaint page actually calls `save_complaint()` after classification.
7. Fix View Complaints page to read from the correct file.
8. Fix Search Complaints page to filter results properly.
9. Fix Analytics page to use the saved complaint data and display charts.
10. After fixes, output corrected code for ALL changed files.

## GOAL

After your fixes, the Streamlit app must work fully:

* Filing a complaint saves it
* Viewing complaints shows them
* Searching works
* Analytics displays accurate charts
* Gemini classification works with no errors
* No model or API errors remain

Now review all files, detect all issues, and rewrite the corrected working code. Provide full runnable files only — do not summarize.

---

**Note to the assistant:** The user will upload the project files or provide access. Use `list_models()` to detect available Gemini models and choose an appropriate model string. Ensure file paths are relative to the project root and create a `data/` folder if necessary. If any changes require environment variables, instruct the user to set them (e.g., `GEMINI_API_KEY` or `MODEL_NAME`).

**End of prompt.**
