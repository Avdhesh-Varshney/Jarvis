import streamlit as st

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.user = []

from src.auth.login import login
def logged_in():
  userData = login()
  if userData != []:
    st.session_state.logged_in = True
    st.session_state.user = userData
    st.rerun()

# /auth
login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# /apps/public
dashboard = st.Page("src/apps/public/dashboard.py", title="Dashboard", icon=":material/dashboard:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

from src.utils.functions import load_functions
if st.session_state.logged_in:
  app = st.navigation(pages=load_functions())
else:
  app = st.navigation({"": [dashboard, youtubePlaylist], "Account": [login_page, sign_up_page]})

app.run()
