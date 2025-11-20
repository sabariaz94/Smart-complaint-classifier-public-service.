import streamlit as st
import pandas as pd
from features.classifier.classifier import classify_complaint
from features.complaints.complaints import save_complaint, load_complaints, search_complaints
from features.analytics.analytics import run as run_analytics
import admin_dashboard

# Page configuration
st.set_page_config(
    page_title="Smart Complaint Classifier",
    page_icon="✅",
    layout="wide",
)

def home():
    """Home page with an overview of the application."""
    st.title("Smart Complaint Classifier Dashboard")
    st.write(
        "This application uses AI to classify public service complaints, "
        "helping to streamline the process of addressing public needs."
    )
    st.info(
        "Use the navigation sidebar on the left to file a new complaint, view "
        "existing ones, search, or see analytics."
    )

def file_complaint_page():
    """Page for users to file a new complaint."""
    st.title("File a New Complaint")
    
    with st.form("complaint_form"):
        complaint_text = st.text_area("Please describe your complaint in detail:", height=150)
        submitted = st.form_submit_button("Submit Complaint")

    if submitted and complaint_text:
        with st.spinner("Analyzing and filing your complaint..."):
            classification = classify_complaint(complaint_text)

            if not classification or "error" in classification:
                st.error(f"Failed to classify the complaint. Error: {classification.get('error', 'Unknown')}")
                return

            # The classifier now adds complaint_text, so we just pass the dict
            save_complaint(classification)

        st.success("Your complaint has been successfully filed and analyzed!")

        # Display the results in a more organized way
        st.subheader("Analysis of Your Complaint")
        
        col1, col2 = st.columns(2)
        col1.metric("Predicted Category", classification.get("category", "N/A"))
        col2.metric("Assigned Priority", classification.get("priority", "N/A"))

        with st.expander("View detailed analysis"):
            st.write(f"**Summary:** {classification.get('summary', 'N/A')}")
            
            keywords = classification.get('keywords', [])
            if keywords:
                st.write("**Keywords:**")
                st.write(", ".join(f"`{k}`" for k in keywords))
                
            confidence = classification.get('confidence')
            if confidence is not None:
                st.write(f"**Confidence Score:** {confidence:.2%}")

def view_complaints_page():
    """Page to view and filter all complaints."""
    st.title("View All Complaints")
    complaints = load_complaints()

    if not complaints:
        st.warning("No complaints have been filed yet.")
        return

    df = pd.DataFrame(complaints)
    
    # Improve DataFrame display
    st.dataframe(
        df,
        column_config={
            "id": st.column_config.TextColumn("ID", width="small"),
            "timestamp": st.column_config.DatetimeColumn("Timestamp", format="YYYY-MM-DD HH:mm"),
            "category": "Category",
            "priority": "Priority",
            "status": "Status",
            "summary": "Summary",
        },
        use_container_width=True
    )

def search_complaints_page():
    """Page to search for specific complaints."""
    st.title("Search Complaints")
    search_query = st.text_input("Enter a keyword to search in complaints:")

    if search_query:
        results = search_complaints(search_query)

        if not results:
            st.info(f"No complaints found matching '{search_query}'.")
        else:
            st.subheader(f"{len(results)} complaints found matching '{search_query}'")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

def main():
    """Main function to run the Streamlit app."""
    st.sidebar.title("Navigation")
    
    # Using icons for a better look
    PAGES = {
        "Home": home,
        "File a Complaint": file_complaint_page,
        "View Complaints": view_complaints_page,
        "Search Complaints": search_complaints_page,
        "Analytics": run_analytics,
        "Admin Dashboard": admin_dashboard.run,
    }
    
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    
    # Run the selected page function
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    # Check for API key and provide a helpful message if it's missing
    try:
        from config import GEMINI_API_KEY
        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
            st.error("Your Gemini API key is not configured. Please set it in your `.env` file.")
            st.stop()
    except (ImportError, ValueError) as e:
        st.error(f"Configuration error: {e}")
        st.stop()
        
    main()