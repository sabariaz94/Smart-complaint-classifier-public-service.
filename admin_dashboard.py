import streamlit as st
import pandas as pd
from config import ADMIN_PASSWORD
from features.complaints.complaints import load_complaints, update_complaint_status

def login():
    """Displays a login form and handles authentication."""
    st.title("Admin Login")
    
    with st.form("login_form"):
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.rerun()  # Use rerun to immediately go to the dashboard
        else:
            st.error("The password you entered is incorrect.")

def dashboard():
    """The main admin dashboard interface."""
    st.title("Admin Dashboard")
    st.write("Here you can manage and update the status of public complaints.")
    
    if st.sidebar.button("Logout"):
        st.session_state["admin_logged_in"] = False
        st.rerun()

    complaints = load_complaints()
    if not complaints:
        st.warning("No complaints have been filed yet.")
        return

    df = pd.DataFrame(complaints)
    
    # Make the display cleaner
    st.subheader("All Complaints")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "id": "ID",
            "timestamp": st.column_config.DatetimeColumn("Timestamp", format="YYYY-MM-DD HH:mm"),
            "complaint_text": st.column_config.TextColumn("Complaint", width="large"),
            "status": "Status",
        },
        hide_index=True,
    )

    st.subheader("Update a Complaint")
    
    # Use a more user-friendly selection box
    # Format: "ID - Summary"
    option_list = [f"{c.get('id')} - {c.get('summary', 'No summary')[:50]}..." for c in complaints]
    selected_option = st.selectbox("Select a complaint to update:", options=option_list)

    if selected_option:
        complaint_id = selected_option.split(" - ")[0]
        
        # Find the full complaint details
        selected_complaint = next((c for c in complaints if c.get("id") == complaint_id), None)

        if selected_complaint:
            with st.form(f"update_{complaint_id}"):
                st.write(f"**Updating Complaint:** `{complaint_id}`")
                
                # Pre-fill with current status
                current_status = selected_complaint.get("status", "New")
                status_options = ["New", "In Progress", "Resolved", "Closed"]
                current_index = status_options.index(current_status) if current_status in status_options else 0

                new_status = st.selectbox(
                    "Set new status:",
                    options=status_options,
                    index=current_index,
                )
                note = st.text_area("Add an internal note (optional):")
                
                update_button = st.form_submit_button("Update Complaint")

                if update_button:
                    update_complaint_status(complaint_id, new_status, note)
                    st.success(f"Complaint `{complaint_id}` updated to **{new_status}**.")
                    # No need to rerun here, will just show the success message
                    # The dataframe will update on the next full rerun if the user navigates
                    st.toast("Complaint updated!")


def run():
    """Runs the admin dashboard, handling login state."""
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        login()
    else:
        dashboard()

if __name__ == "__main__":
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
    try:
        from config import ADMIN_PASSWORD
        if not ADMIN_PASSWORD:
            st.error("Admin password is not configured. Please set it in your .env file.")
            st.stop()
    except (ImportError, ValueError) as e:
        st.error(f"Configuration error: {e}")
        st.stop()
    run()