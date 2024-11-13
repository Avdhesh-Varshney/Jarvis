from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from datetime import datetime, timedelta
import streamlit as st

today = datetime.now()

def logged_in():
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

def login():
	userData, password, remember_me = logged_in()

	if userData != []:
		conn = server()
		user = [userData['username'], userData['email'], userData['first_name'], userData['last_name'], userData['role'], userData['gender'], userData['age'], userData['about']]

		conn.setLocalStorageVal("user", user)
		conn.setLocalStorageVal("password", password)
		conn.setLocalStorageVal("expiration_date", (today + timedelta(days=(30 if remember_me else 1))).isoformat())
		conn.setLocalStorageVal("verified", True)
		st.rerun()
