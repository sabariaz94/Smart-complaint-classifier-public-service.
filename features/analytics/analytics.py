import streamlit as st
import pandas as pd
import plotly.express as px
from features.complaints.complaints import load_complaints

def run():
    """
    Runs the Streamlit analytics dashboard.
    """
    st.title("Complaints Analytics Dashboard")

    complaints = load_complaints()

    if not complaints:
        st.warning("No complaints data found.")
        return

    df = pd.DataFrame(complaints)

    # --- KPIs ---
    total_complaints = len(df)
    high_priority_complaints = len(df[df["priority"] == "High"])
    unique_categories = df["category"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints", total_complaints)
    col2.metric("High Priority Complaints", high_priority_complaints)
    col3.metric("Unique Categories", unique_categories)

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)

    # Bar chart of complaints per category
    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]
    fig_cat = px.bar(
        category_counts,
        x="category",
        y="count",
        title="Complaints per Category",
        labels={"category": "Category", "count": "Number of Complaints"},
    )
    col1.plotly_chart(fig_cat, use_container_width=True)

    # Pie chart of complaints by priority
    priority_counts = df["priority"].value_counts().reset_index()
    priority_counts.columns = ["priority", "count"]
    fig_prio = px.pie(
        priority_counts,
        values="count",
        names="priority",
        title="Complaints by Priority",
    )
    col2.plotly_chart(fig_prio, use_container_width=True)

    st.markdown("---")

    # --- Data Table ---
    st.subheader("Latest Complaints")
    st.dataframe(df[["timestamp", "complaint_text", "category", "priority", "summary"]].sort_values("timestamp", ascending=False).head(10))


if __name__ == "__main__":
    st.set_page_config(page_title="Complaints Analytics", layout="wide")
    run()
