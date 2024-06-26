import streamlit as st
from database.sql import create_connection, create_usertable, login_user

def login():
  st.title("🔐 Login")
  st.subheader("Welcome Back!")
  st.markdown("Please enter your username/email and password to log in.")

  # Input fields for username/email and password
  user = st.text_input("👤 Username/Email:")
  password = st.text_input("🔑 Password:", type="password")

  if st.button("Log in"):
    conn = create_connection()
    create_usertable(conn)
    result = login_user(conn, user, password)
    if result:
      st.success("Logged in as {}!".format(result[0][3]), icon="✅")
      return result
    else:
      st.warning("Incorrect credentials!")
  return []
