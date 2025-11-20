# Smart Complaint Classifier for Public Services

A professional CLI application that classifies public-service complaints (e.g., electricity, water, roads, waste management) using an AI model (Gemini).
The system helps government/public-service teams automatically categorize complaints and store them for further processing.

## Core Features

- **Complaint submission via CLI**: File a new complaint directly from the command line.
- **AI-powered complaint classification (Gemini API)**: Automatically classify complaints into categories and determine their priority.
- **Multi-class categories**: `Electricity`, `Water`, `Roads`, `Waste`, `Health`, `Security`, `Other`.
- **Priority detection**: `High`, `Medium`, `Low`.
- **Complaint history storage**: All complaints are stored in a local JSON file.
- **Search & filter complaints**: Search for complaints by keyword.
- **CSV/JSON export**: Export all complaints to a CSV or JSON file.
- **Simple Streamlit dashboard**: An optional dashboard for visualizing complaint trends and stats.

## Tech Stack

- **Language**: Python 3.11+
- **CLI Framework**: `questionary`
- **UI Library**: `rich`
- **AI Model**: Gemini API
- **Storage**: JSON file
- **Dashboard**: `streamlit`, `pandas`, `plotly`
- **Package Manager**: `uv`

## Project Structure

```
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
    └── analytics/
        ├── GEMINI.md
        └── analytics.py          # Stats, trending issues
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/smart-complaint-classifier.git
   cd smart-complaint-classifier
   ```

2. **Create a virtual environment and install dependencies**:
   - Using `uv`:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
     uv pip install -r requirements.txt 
     ```
   - If you don't have `uv` installed, you can install it with `pip install uv`.

3. **Set up your Gemini API Key**:
   - Rename the `.env.example` file to `.env`.
   - Open the `.env` file and replace `YOUR_API_KEY` with your actual Gemini API key.
     - **Important**: The error `API key not valid` indicates that your `GEMINI_API_KEY` in the `.env` file is incorrect or missing. Please ensure you have replaced `YOUR_API_KEY` with a valid key obtained from Google AI Studio.

## Usage

**CLI Application:**

Run the CLI application with the following command:

```bash
uv run main.py
```

This will launch the interactive CLI menu.

**Streamlit Web Application:**

To run the Streamlit web application, use the following command:

```bash
streamlit run streamlit_app.py
```

This will open the analytics dashboard in your web browser.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.