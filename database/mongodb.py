from database.encrypt import check_password
from pymongo import MongoClient
import streamlit as st
import pandas as pd
import re

def URI_Exist():
	if st.secrets["general"]["MONGODB_URI"] != "":
		return True
	return False

######################### Checking validations #########################

def valid_username(username):
	return re.match(r'^[a-zA-Z0-9]+$', username) is not None

def valid_email(email):
	return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

######################### DB Management #########################

def create_connection():
	if URI_Exist():
		MONGODB_URI = st.secrets["general"]["MONGODB_URI"]
	else:
		MONGODB_URI = "mongodb://localhost:27017/"
	client = MongoClient(MONGODB_URI)
	db = client['user_db']
	return db

conn = create_connection()

def add_userdata(conn, username, firstname, lastname, role, gender, age, email, about, password):
	users_collection = conn['users_records']
	user_data = {
		"username": username,
		"first_name": firstname,
		"last_name": lastname,
		"role": role,
		"gender": gender,
		"age": age,
		"email": email,
		"about": about,
		"password": password
	}
	users_collection.insert_one(user_data)

def get_password(conn, text):
	users_collection = conn['users_records']
	if valid_email(text):
		user = users_collection.find_one({"email": text})
	elif valid_username(text):
		user = users_collection.find_one({"username": text})

	return user['password'] if user else ""

def login_user(conn, text, password):
	hashed_password = get_password(conn, text)
	if not hashed_password:
		return None

	try:
		correct_pwd = check_password(password, hashed_password)
	except:
		return None

	if correct_pwd:
		users_collection = conn['users_records']
		if valid_email(text):
			user = users_collection.find_one({"email": text, "password": hashed_password})
		elif valid_username(text):
			user = users_collection.find_one({"username": text, "password": hashed_password})
		return user
	return None

def check_user(conn, text):
	users_collection = conn['users_records']
	if valid_email(text):
		user = users_collection.find_one({"email": text})
	elif valid_username(text):
		user = users_collection.find_one({"username": text})
	return user

def view_all_users(conn):
	users_collection = conn['users_records']
	users = users_collection.find()
	return list(users)

######################### Data Engagement #########################

def show_data():
	conn = create_connection()
	users = view_all_users(conn)
	df = pd.DataFrame(users, columns=['_id', 'username', 'first_name', 'last_name', 'role', 'gender', 'age', 'email', 'about', 'password'])
	df['_id'] = df['_id'].astype(str)
	return df
