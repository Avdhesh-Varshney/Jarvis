from database.mongodb import valid_email, valid_username, create_connection, add_userdata, check_user
from database.encrypt import secure_password
from database.localStorageServer import server
from datetime import datetime, timedelta
import streamlit as st
import re

today = datetime.now()

# Password Strength Validation Function
def validate_password_strength(password):
	if len(password) < 8:
		return "Password must be at least 8 characters long!"
	if not re.search(r"\d", password):
		return "Password must contain at least one digit!"
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
		return "Password must contain at least one special character!"
	return None

def signup():
	st.title("🔐 Signup Form")
	st.subheader("Create a New Account")
	st.markdown("Please fill out the form below to create a new account.")

	# Personal Information Section
	st.markdown("## Personal Information")
	colx, coly = st.columns(2)
	with colx:
		first_name = st.text_input("👤 Enter your first name:")
	with coly:
		last_name = st.text_input("👤 Enter your last name:")
	new_email = st.text_input("📧 Enter your email:")
	new_about = st.text_area("💬 About yourself:")
	new_age = st.slider('🎂 Enter your age:', 5, 100, today.year-2002)

	# Account Details Section
	st.markdown("## Account Details")
	new_user = st.text_input("👥 Create your username:")

	col1, col2 = st.columns(2)
	with col1:
		new_gender = st.radio('⚧ Select your gender:', ['Male', 'Female', 'Other'])
	with col2:
		new_roles = st.selectbox("👔 Select your role:", ["User", "Admin"])

	# Password Section
	st.markdown("## Password")
	col3, col4 = st.columns(2)
	with col3:
		new_password = st.text_input("🔑 Enter password:", type='password')
	with col4:
		new_repeat_password = st.text_input('🔑 Re-type your password:', type='password')

	# Handle Role-Based Key Inputs
	admin_key = st.secrets["ADMIN_KEY"]

	if new_roles == 'Admin':
		pass_key = st.text_input('🔑 Enter your Admin key:')
		if pass_key != admin_key:
			st.warning("Invalid admin key!", icon="⚠️")
			return

	remember_me = st.checkbox("Remember me for 30 days", value=False, key="remember_me_key")

	st.markdown("---")
	if st.button("Signup"):
		if not first_name or not last_name or not new_email or not new_user or not new_password or not new_repeat_password:
			st.warning("Please fill out all mandatory fields!", icon="⚠️")
			return

		if new_password != new_repeat_password:
			st.warning("Passwords do not match!", icon="⚠️")
			return
		
		if validate_password_strength(new_password):
			st.warning(validate_password_strength(new_password), icon="⚠️")
			return

		new_password_hashed = secure_password(new_password)
		if not valid_email(new_email):
			st.warning("Invalid email address!", icon="⚠️")
			return

		if not valid_username(new_user):
			st.warning("Invalid username!", icon="⚠️")
			return

		conn = create_connection()
		if check_user(conn, new_email) or check_user(conn, new_user):
			st.warning("Email or username already exists. Please choose another!", icon="⚠️")
			return

		if not new_about:
			st.warning("Please provide some information about yourself!", icon="⚠️")
			return

		add_userdata(conn, new_user, first_name, last_name, new_roles, new_gender, new_age, new_email, new_about, new_password_hashed)

		user = [new_user, new_email, first_name, last_name, new_roles, new_gender, new_age, new_about]
		conn = server()
		conn.setLocalStorageVal("user", user)
		conn.setLocalStorageVal("password", new_password)
		conn.setLocalStorageVal("expiration_date", (today + timedelta(days=(30 if remember_me else 1))).isoformat())
		conn.setLocalStorageVal("verified", True)

		st.success("You have successfully created a valid account!", icon="✅")
		st.info("Go to Login Menu to login!", icon="ℹ️")
		st.info("Please refresh the page to continue", icon="ℹ️")
