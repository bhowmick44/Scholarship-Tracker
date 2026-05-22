import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# --- 1. DATABASE SETUP ---
# --- 1. DATABASE SETUP ---
conn = sqlite3.connect("scholarships.db", check_same_thread=False)
conn = sqlite3.connect("scholarships.db", check_same_thread=False)
cursor = conn.cursor()
cursor = conn.cursor()


cursor.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, university TEXT, scholarship TEXT, opening_date TEXT, deadline TEXT, status TEXT, link TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, university TEXT, scholarship TEXT, opening_date TEXT, deadline TEXT, status TEXT, link TEXT)")
conn.commit()
conn.commit()


# --- 2. APP INTERFACE ---
# --- 2. APP INTERFACE ---
st.set_page_config(page_title="Scholarship Tracker", page_icon="🎓", layout="wide")
st.set_page_config(page_title="Scholarship Tracker", page_icon="🎓", layout="wide")
st.title("🎓 Scholarship Tracker")
st.title("🎓 Scholarship Tracker")


tab1, tab2, tab3, tab4 = st.tabs([
tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Uni", 
    "➕ Add Uni", 
    "🟢 Opening Soon (30 Days)", 
    "🟢 Opening Soon (30 Days)", 
    "🔴 Ending Soon (15 Days)", 
    "🔴 Ending Soon (15 Days)", 
    "📋 All Saved Links"
    "📋 All Saved Links"
])
])


with tab1:
with tab1:
    st.header("Add New Application")
    st.header("Add New Application")
    with st.form("add_form", clear_on_submit=True):
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1, col2 = st.columns(2)
        
        
        with col1:
        with col1:
            uni = st.text_input("University Name")
            uni = st.text_input("University Name")
            scholar = st.text_input("Scholarship Name")
            scholar = st.text_input("Scholarship Name")
            link = st.text_input("Application URL (Link)")
            link = st.text_input("Application URL (Link)")
            
            
        with col2:
        with col2:
            opening_date = st.date_input("Opening Date")
            opening_date = st.date_input("Opening Date")
            deadline = st.date_input("Deadline")
            deadline = st.date_input("Deadline")
            status = st.selectbox("Status", ["Researching", "Drafting Essay", "Applied", "Accepted"])
            status = st.selectbox("Status", ["Researching", "Drafting Essay", "Applied", "Accepted"])
        
        
        submit = st.form_submit_button("Save to Database")
        submit = st.form_submit_button("Save to Database")


        if submit:
        if submit:
            cursor.execute("INSERT INTO applications (university, scholarship, opening_date, deadline, status, link) VALUES (?, ?, ?, ?, ?, ?)",
            cursor.execute("INSERT INTO applications (university, scholarship, opening_date, deadline, status, link) VALUES (?, ?, ?, ?, ?, ?)",
                      (uni, scholar, str(opening_date), str(deadline), status, link))
                      (uni, scholar, str(opening_date), str(deadline), status, link))
            conn.commit()
            conn.commit()
            st.success(f"Successfully added {uni}!")
            st.success(f"Successfully added {uni}!")
            st.rerun()
            st.rerun()


df = pd.read_sql_query("SELECT * FROM applications", conn)
df = pd.read_sql_query("SELECT * FROM applications", conn)


if not df.empty:
if not df.empty:
    df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce').dt.date
    df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce').dt.date
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
    df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce').dt.date
    
    
    today = datetime.today().date()
    today = datetime.today().date()
    thirty_days_ago = today - timedelta(days=30)
    thirty_days_ago = today - timedelta(days=30)
    fifteen_days_from_now = today + timedelta(days=15)
    fifteen_days_from_now = today + timedelta(days=15)


    with tab2:
    with tab2:
        st.header("🟢 Recently Opened & Coming Soon")
        st.header("🟢 Recently Opened & Coming Soon")
        coming_df = df[(df['opening_date'] >= thirty_days_ago) & (df['opening_date'] <= today)]
        coming_df = df[(df['opening_date'] >= thirty_days_ago) & (df['opening_date'] <= today)]
        if not coming_df.empty:
        if not coming_df.empty:
            st.dataframe(coming_df, hide_index=True, use_container_width=True)
            st.dataframe(coming_df, hide_index=True, use_container_width=True)
        else:
        else:
            st.info("No applications opened in the last 30 days.")
            st.info("No applications opened in the last 30 days.")


    with tab3:
    with tab3:
        st.header("🔴 Deadlines Approaching")
        st.header("🔴 Deadlines Approaching")
        ending_df = df[(df['deadline'] >= today) & (df['deadline'] <= fifteen_days_from_now)]
        ending_df = df[(df['deadline'] >= today) & (df['deadline'] <= fifteen_days_from_now)]
        if not ending_df.empty:
        if not ending_df.empty:
            st.dataframe(ending_df, hide_index=True, use_container_width=True)
            st.dataframe(ending_df, hide_index=True, use_container_width=True)
        else:
        else:
            st.success("You have no deadlines in the next 15 days. Breathe easy!")
            st.success("You have no deadlines in the next 15 days. Breathe easy!")


    with tab4:
    with tab4:
        st.header("📋 All Saved Applications")
        st.header("📋 All Saved Applications")
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.divider()
        st.divider()
        
        
        # --- THE SIDE-BY-SIDE LAYOUT ---
        # --- THE SIDE-BY-SIDE LAYOUT ---
        col_edit, col_delete = st.columns(2)
        col_edit, col_delete = st.columns(2)
        
        
        with col_edit:
        with col_edit:
            st.subheader("✏️ Edit an Entry")
            st.subheader("✏️ Edit an Entry")
            edit_id = st.selectbox("Select ID to Edit:", df['id'], key="edit_select")
            edit_id = st.selectbox("Select ID to Edit:", df['id'], key="edit_select")
            
            
            # Fetch the existing data for the selected ID
            # Fetch the existing data for the selected ID
            edit_record = df[df['id'] == edit_id].iloc[0]
            edit_record = df[df['id'] == edit_id].iloc[0]
            
            
            with st.form("edit_form"):
            with st.form("edit_form"):
                e_uni = st.text_input("University Name", value=edit_record['university'])
                e_uni = st.text_input("University Name", value=edit_record['university'])
                e_scholar = st.text_input("Scholarship Name", value=edit_record['scholarship'])
                e_scholar = st.text_input("Scholarship Name", value=edit_record['scholarship'])
                
                
                # Safely grab the link (or leave blank if it doesn't exist)
                # Safely grab the link (or leave blank if it doesn't exist)
                current_link = edit_record['link'] if pd.notnull(edit_record['link']) else ""
                current_link = edit_record['link'] if pd.notnull(edit_record['link']) else ""
                e_link = st.text_input("Application URL (Link)", value=current_link)
                e_link = st.text_input("Application URL (Link)", value=current_link)
                
                
                # Safely load the status dropdown
                # Safely load the status dropdown
                status_list = ["Researching", "Drafting Essay", "Applied", "Accepted"]
                status_list = ["Researching", "Drafting Essay", "Applied", "Accepted"]
                current_status = edit_record['status']
                current_status = edit_record['status']
                current_status_index = status_list.index(current_status) if current_status in status_list else 0
                current_status_index = status_list.index(current_status) if current_status in status_list else 0
                e_status = st.selectbox("Status", status_list, index=current_status_index)
                e_status = st.selectbox("Status", status_list, index=current_status_index)
                
                
                # Safely load dates, default to today if there is a blank entry
                # Safely load dates, default to today if there is a blank entry
                o_date = edit_record['opening_date'] if pd.notnull(edit_record['opening_date']) else today
                o_date = edit_record['opening_date'] if pd.notnull(edit_record['opening_date']) else today
                d_date = edit_record['deadline'] if pd.notnull(edit_record['deadline']) else today
                d_date = edit_record['deadline'] if pd.notnull(edit_record['deadline']) else today
                
                
                e_opening = st.date_input("Opening Date", value=o_date, key="e_open")
                e_opening = st.date_input("Opening Date", value=o_date, key="e_open")
                e_deadline = st.date_input("Deadline", value=d_date, key="e_dead")
                e_deadline = st.date_input("Deadline", value=d_date, key="e_dead")
                
                
                update_btn = st.form_submit_button("Update Application")
                update_btn = st.form_submit_button("Update Application")
                
                
                if update_btn:
                if update_btn:
                    cursor.execute("UPDATE applications SET university=?, scholarship=?, opening_date=?, deadline=?, status=?, link=? WHERE id=?", 
                    cursor.execute("UPDATE applications SET university=?, scholarship=?, opening_date=?, deadline=?, status=?, link=? WHERE id=?", 
                                  (e_uni, e_scholar, str(e_opening), str(e_deadline), e_status, e_link, edit_id))
                                  (e_uni, e_scholar, str(e_opening), str(e_deadline), e_status, e_link, edit_id))
                    conn.commit()
                    conn.commit()
                    st.success("Updated successfully!")
                    st.success("Updated successfully!")
                    st.rerun()
                    st.rerun()


        with col_delete:
        with col_delete:
            st.subheader("🗑️ Delete an Entry")
            st.subheader("🗑️ Delete an Entry")
            delete_id = st.selectbox("Select ID to Delete:", df['id'], key="del_select")
            delete_id = st.selectbox("Select ID to Delete:", df['id'], key="del_select")
            
            
            # The type="primary" makes the button red/highlighted
            # The type="primary" makes the button red/highlighted
            if st.button("Delete Application", type="primary"):
            if st.button("Delete Application", type="primary"):
                cursor.execute("DELETE FROM applications WHERE id = ?", (delete_id,))
                cursor.execute("DELETE FROM applications WHERE id = ?", (delete_id,))
                conn.commit()
                conn.commit()
                st.rerun()
                st.rerun()


else:
else:
    with tab2:
    with tab2:
        st.info("No applications added yet.")
        st.info("No applications added yet.")
    with tab3:
    with tab3:
        st.info("No applications added yet.")
        st.info("No applications added yet.")
    with tab4:
    with tab4:
        st.info("No applications added yet.")
        st.info("No applications added yet.")
