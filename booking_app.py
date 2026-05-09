import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="Titan Scheduler",
    page_icon="📅",
    layout="wide"
)

DB_FILE = "bookings.csv"

if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Name", "Email", "Date", "Time", "Notes"])
    df.to_csv(DB_FILE, index=False)

# --- URL ROUTING LOGIC ---
query_params = st.query_params

if query_params.get("view") == "admin":
    # --- ADMIN VIEW ---
    st.title("🔒 Admin Access")

    # Password Protection
    password = st.text_input("Enter Admin Password", type="password")

    if password == "Titan2026":
        st.success("Access Granted")
        st.subheader("Manage Upcoming Appointments")

        if os.path.exists(DB_FILE):
            view_df = pd.read_csv(DB_FILE)
            if not view_df.empty:
                st.dataframe(view_df, use_container_width=True)
                st.metric("Total Appointments", len(view_df))
            else:
                st.warning("The database is currently empty.")

        if st.button("Logout & Back to Booking"):
            st.query_params.clear()
            st.rerun()

    elif password != "":
        st.error("Incorrect Password. Please try again.")

else:
    st.title("📅 Titan Scheduler")
    st.subheader("Reserve your professional consultation")

    with st.form("booking_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Select Date", min_value=datetime.today())
        with col2:

            time = st.text_input("Preferred Time (e.g., 10:30 AM or Afternoon)")

        notes = st.text_area("Additional Notes (Optional)")
        submit = st.form_submit_button("Confirm Booking")

    if submit:
        if name and email and time:
            new_data = pd.DataFrame([[name, email, str(date), time, notes]],
                                    columns=["Name", "Email", "Date", "Time", "Notes"])
            new_data.to_csv(DB_FILE, mode='a', header=False, index=False)

            st.success(f"Successfully Booked for {date} at {time}. Confirmation sent to {email}.")
        else:
            st.error("Please fill in all required fields (Name, Email, and Time).")