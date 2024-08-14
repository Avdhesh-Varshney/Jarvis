import streamlit as st
from database.mongodb import create_connection, login_user

def login():
  st.title("🔐 Login")
  st.subheader("Welcome Back!")
  st.markdown("Please enter your username/email and password to log in.")

  # Input fields for username/email and password
  user = st.text_input("👤 Username/Email:")
  password = st.text_input("🔑 Password:", type="password")

  if st.button("Log in") and user and password:
    conn = create_connection()
    result = login_user(conn, user, password)
    if result:
      st.success(f"Logged in as {result['role']}!", icon="✅")
      return result
    else:
      st.warning("Incorrect credentials!", icon="⚠️")
  return []
