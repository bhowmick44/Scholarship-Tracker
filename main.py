import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect("scholarships.db", check_same_thread=False)
cursor = conn.cursor()

# I removed the triple quotes and put this on one clean line to prevent copy-paste errors
cursor.execute(
    "CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, university TEXT, scholarship TEXT, opening_date TEXT, deadline TEXT, status TEXT, link TEXT)")
conn.commit()

# --- 2. APP INTERFACE ---
st.set_page_config(page_title="Scholarship Tracker", page_icon="🎓", layout="wide")
st.title("🎓 Scholarship Tracker")

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Uni",
    "🟢 Opening Soon (30 Days)",
    "🔴 Ending Soon (15 Days)",
    "📋 All Saved Links"
])

with tab1:
    st.header("Add New Application")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            uni = st.text_input("University Name")
            scholar = st.text_input("Scholarship Name")
            link = st.text_input("Application URL (Link)")

        with col2:
            opening_date = st.date_input("Opening Date")
            deadline = st.date_input("Deadline")
            status = st.selectbox("Status", ["Researching", "Drafting Essay", "Applied", "Accepted"])

        submit = st.form_submit_button("Save to Database")

        if submit:
            cursor.execute(
                "INSERT INTO applications (university, scholarship, opening_date, deadline, status, link) VALUES (?, ?, ?, ?, ?, ?)",
                (uni, scholar, str(opening_date), str(deadline), status, link))
            conn.commit()
            st.success(f"Successfully added {uni}!")
            st.rerun()

df = pd.read_sql_query("SELECT * FROM applications", conn)

if not df.empty:
    df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce').dt.date
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date

    today = datetime.today().date()
    thirty_days_ago = today - timedelta(days=30)
    fifteen_days_from_now = today + timedelta(days=15)

    with tab2:
        st.header("🟢 Recently Opened & Coming Soon")
        coming_df = df[(df['opening_date'] >= thirty_days_ago) & (df['opening_date'] <= today)]
        if not coming_df.empty:
            st.dataframe(coming_df, hide_index=True, use_container_width=True)
        else:
            st.info("No applications opened in the last 30 days.")

    with tab3:
        st.header("🔴 Deadlines Approaching")
        ending_df = df[(df['deadline'] >= today) & (df['deadline'] <= fifteen_days_from_now)]
        if not ending_df.empty:
            st.dataframe(ending_df, hide_index=True, use_container_width=True)
        else:
            st.success("You have no deadlines in the next 15 days. Breathe easy!")

    with tab4:
        st.header("📋 All Saved Applications")
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.divider()
        st.subheader("🗑️ Delete an Entry")
        delete_id = st.selectbox("Select ID to Delete:", df['id'], key="del_select")
        if st.button("Delete Application", type="primary"):
            cursor.execute("DELETE FROM applications WHERE id = ?", (delete_id,))
            conn.commit()
            st.rerun()
else:
    with tab2:
        st.info("No applications added yet.")
    with tab3:
        st.info("No applications added yet.")
    with tab4:
        st.info("No applications added yet.")