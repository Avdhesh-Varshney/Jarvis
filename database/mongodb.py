from database.encrypt import check_password
from pymongo import MongoClient, errors
import streamlit as st
import pandas as pd
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

######################### Utility Functions #########################

def URI_Exist():
    return st.secrets["general"].get("MONGODB_URI", "") != ""

######################### Input Validation #########################

def valid_username(username):
    return re.match(r'^[a-zA-Z0-9]+$', username) is not None

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def valid_age(age):
    try:
        age = int(age)
        return 0 <= age <= 120
    except ValueError:
        return False

######################### DB Management #########################

def create_connection():
    try:
        if URI_Exist():
            MONGODB_URI = st.secrets["general"]["MONGODB_URI"]
        else:
            MONGODB_URI = "mongodb://localhost:27017/"
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger connection check
        db = client['user_db']
        logging.info("Database connection established successfully.")
        return db
    except errors.ServerSelectionTimeoutError as e:
        logging.error(f"Database connection failed: {e}")
        st.error("Unable to connect to the database. Please check the connection settings.")
        return None

def add_userdata(conn, username, firstname, lastname, role, gender, age, email, about, password):
    if not valid_username(username) or not valid_email(email) or not valid_age(age):
        logging.warning("Invalid input data for adding user.")
        st.error("Invalid input data. Please check your entries.")
        return

    try:
        users_collection = conn['users_records']
        user_data = {
            "username": username,
            "first_name": firstname,
            "last_name": lastname,
            "role": role,
            "gender": gender,
            "age": int(age),
            "email": email,
            "about": about,
            "password": password
        }
        users_collection.insert_one(user_data)
        logging.info(f"User {username} added successfully.")
    except errors.DuplicateKeyError:
        logging.error("Duplicate entry detected.")
        st.error("A user with the same username or email already exists.")
    except Exception as e:
        logging.error(f"Failed to add user: {e}")
        st.error("An error occurred while adding the user.")

def get_password(conn, text):
    try:
        users_collection = conn['users_records']
        if valid_email(text):
            user = users_collection.find_one({"email": text})
        elif valid_username(text):
            user = users_collection.find_one({"username": text})
        return user['password'] if user else ""
    except Exception as e:
        logging.error(f"Error retrieving password: {e}")
        return ""

def login_user(conn, text, password):
    try:
        hashed_password = get_password(conn, text)
        if not hashed_password:
            return None
        correct_pwd = check_password(password, hashed_password)
        if correct_pwd:
            users_collection = conn['users_records']
            if valid_email(text):
                return users_collection.find_one({"email": text, "password": hashed_password})
            elif valid_username(text):
                return users_collection.find_one({"username": text, "password": hashed_password})
        return None
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return None

def view_all_users(conn):
    try:
        users_collection = conn['users_records']
        users = users_collection.find()
        return list(users)
    except Exception as e:
        logging.error(f"Error retrieving users: {e}")
        st.error("An error occurred while fetching user data.")
        return []

######################### Data Engagement #########################

def show_data():
    conn = create_connection()
    if not conn:
        return pd.DataFrame()
    users = view_all_users(conn)
    if not users:
        return pd.DataFrame()
    df = pd.DataFrame(users, columns=['_id', 'username', 'first_name', 'last_name', 'role', 'gender', 'age', 'email', 'about', 'password'])
    df['_id'] = df['_id'].astype(str)
    return df
