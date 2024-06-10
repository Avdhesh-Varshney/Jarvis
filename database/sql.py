import sqlite3
import re

from page.auth.encrypt import check_password

######################### Checking validations #########################
def valid_username(username):
    return re.match(r'^[a-zA-Z0-9]+$', username) is not None

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

######################### DB Management #########################
def create_connection():
    return sqlite3.connect("database/data.db")

conn = create_connection()

def create_usertable(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users_data(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			name TEXT NOT NULL,
		    role TEXT NOT NULL,
			gender TEXT NOT NULL,
			age INTEGER NOT NULL,
			email TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL
		)
	''')

def add_userdata(conn, username, name, role, gender, age, email, password):
    c = conn.cursor()
    c.execute('INSERT INTO users_data(username, name, role, gender, age, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', 
		   (username, name, role, gender, age, email, password))
    conn.commit()

def login_user(conn, text, password):
    c = conn.cursor()
    hashed_password = get_password(c, text)
    try:
        correct_pwd = check_password(password, hashed_password)
    except:
        return None
    if valid_email(text):
        c.execute('SELECT * FROM users_data WHERE email = ? AND password = ?', (text, hashed_password))
    elif valid_username(text):
        c.execute('SELECT * FROM users_data WHERE username = ? AND password = ?', (text, hashed_password))
    if correct_pwd:
        data = c.fetchall()
        return data

def get_password(conn, text):
    c = conn
    if valid_email(text):
        res = c.execute('SELECT password FROM users_data WHERE email = ?', (text,))
    elif valid_username(text):
        res = c.execute('SELECT password FROM users_data WHERE username = ?', (text,))
    try:
        data = res.fetchone()[0]
    except:
        data = b""
    return data

def check_user(conn, text):
    c = conn.cursor()
    if valid_email(text):
        c.execute('SELECT * FROM users_data WHERE email = ?', (text,))
    elif valid_username(text):
        c.execute('SELECT * FROM users_data WHERE username = ?', (text,))
    data = c.fetchall()
    return data

def view_all_users(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM users_data')
    data = c.fetchall()
    return data
