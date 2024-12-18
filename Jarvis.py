import streamlit as st
from datetime import datetime, timedelta
from src.auth.login import login
from src.utils.functions import load_functions
from database.localStorageServer import server

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = []

# Login and session management
if not st.session_state.logged_in:
    user_data, password, remember_me = login()
    if user_data:
        st.session_state.logged_in = True
        st.session_state.user = user_data
        conn = server()
        conn.setLocalStorageVal("user", user_data)
        conn.setLocalStorageVal("password", password)
        conn.setLocalStorageVal("expiration_date", (datetime.now() + timedelta(days=(30 if remember_me else 1))).isoformat())
        conn.setLocalStorageVal("verified", True)
        st.rerun()

# Application pages
if st.session_state.logged_in:
    app = st.navigation(pages=load_functions())
else:
    app = st.navigation({"": [st.Page("src/apps/public/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
                               st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")],
                          "Account": [st.Page(login, title="Log in", icon=":material/login:"),
                                       st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")]})

app.run()
