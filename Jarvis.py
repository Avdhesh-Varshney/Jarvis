from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from datetime import datetime, timedelta
import streamlit as st

today = datetime.now()

if "user" not in st.session_state:
  st.session_state['password'] = None
  st.session_state["user"] = ['', '', '', '', '', '', '', '']
  st.session_state['expiration_date'] = (today - timedelta(days=10)).isoformat()
  st.session_state['verified'] = False

def getCredentials():
  conn = server()
  return conn.getLocalStorageVal("password"), conn.getLocalStorageVal("user"), conn.getLocalStorageVal("expiration_date"), conn.getLocalStorageVal("verified")

def logged_in():
  from src.auth.login import login
  userData, password, remember_me = login()

  if userData != []:
    conn = server()
    user = [userData['username'], userData['email'], userData['first_name'], userData['last_name'], userData['role'], userData['gender'], userData['age'], userData['about']]

    conn.setLocalStorageVal("user", user)
    conn.setLocalStorageVal("password", password)
    conn.setLocalStorageVal("expiration_date", (today + timedelta(days=(30 if remember_me else 1))).isoformat())
    conn.setLocalStorageVal("verified", True)
    st.info("Please refresh the page to continue", icon="ℹ️")

def application():
  # /apps/public
  home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
  youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

  # /auth
  login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
  sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")
  return st.navigation({"": [home, youtubePlaylist], "Account": [login_page, sign_up_page]})

if __name__ == "__main__":
  app = application()

  if st.session_state['password'] is None:
    st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = getCredentials()

  if st.session_state['password'] is not None and st.session_state['expiration_date'] > today.isoformat():
    if not st.session_state['verified']:
      conn = create_connection()
      result = login_user(conn, st.session_state['user'].split(',')[0], st.session_state['password'])
      if result:
        st.session_state['verified'] = True
        conn = server()
        conn.setLocalStorageVal("verified", True)
    if st.session_state['verified']:
      from src.utils.functions import load_functions
      app = st.navigation(pages=load_functions())

app.run()
