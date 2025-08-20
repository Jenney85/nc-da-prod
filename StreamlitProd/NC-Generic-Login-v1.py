import streamlit as st
import pandas as pd

@st.cache_data
def load_permissions():
    return pd.read_csv("permissions.csv")

st.set_page_config(page_title="Nature Counter DATAframe Login", layout="centered")
st.title("🔐 NC DATA Dashboard Login")

email = st.text_input("Enter your email:").strip().lower()
if email:
    permissions = load_permissions()
    match = permissions[permissions["email"].str.lower() == email]

    if match.empty:
        st.error("Email not found. Access denied.")
    else:
        st.session_state["user_email"] = email
        st.session_state["user_role"] = match.iloc[0]["role"]
        st.success(f"Welcome! You are logged in: {email} | {match.iloc[0]['role']}")
        st.info("Please use the sidebar to view your dashboard.")
