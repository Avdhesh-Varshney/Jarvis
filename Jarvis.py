import streamlit as st

if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.username = ""
  st.session_state.name = ""
  st.session_state.role = ""
  st.session_state.gender = ""
  st.session_state.age = 5
  st.session_state.email = ""
  st.session_state.about = ""

from src.auth.login import login
def logged_in():
  userData = login()
  if userData != []:
    st.session_state.logged_in = True
    st.session_state.username = userData[0][1]
    st.session_state.name = userData[0][2]
    st.session_state.role = userData[0][3]
    st.session_state.gender = userData[0][4]
    st.session_state.age = userData[0][5]
    st.session_state.email = userData[0][6]
    st.session_state.about = userData[0][7]
    st.rerun()

# /auth
login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# /apps
dashboard = st.Page("src/apps/dashboard.py", title="Dashboard", icon=":material/dashboard:")


from src.utils.functions import load_functions
if st.session_state.logged_in:
  app = st.navigation(pages=load_functions())
else:
  app = st.navigation({"": [dashboard], "Account": [login_page, sign_up_page]})

app.run()
