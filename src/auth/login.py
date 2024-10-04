import streamlit as st
from database.mongodb import create_connection, login_user

def login():
  st.title("🔐 Login")
  st.subheader("Welcome Back!")
  st.markdown("Please enter your username/email and password to log in.")

  # Input fields for username/email and password
  user = st.text_input("👤 Username/Email:")
  password = st.text_input("🔑 Password:", type="password")
  remember_me = st.checkbox("Remember me for 30 days", value=False, key="remember_me_key")

  if st.button("Log in") and user and password:
    conn = create_connection()
    result = login_user(conn, user, password)
    if result:
      st.success(f"Credentials Saved for {30 if remember_me else 1} day's!", icon="✅")
      return result, password, remember_me
    else:
      st.warning("Incorrect credentials!", icon="⚠️")
  return [], password, remember_me
