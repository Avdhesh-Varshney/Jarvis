import streamlit as st
from streamlit.components.v1 import html

html(f'''
     <script defer src="https://cloud.umami.is/script.js" data-website-id={st.secrets["UMAMI_WEBSITE_ID"]}></script>
     ''', width=0, height=0, scrolling=False
    )

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

# /apps
dashboard = st.Page("src/apps/dashboard.py", title="Dashboard", icon=":material/dashboard:")


from src.utils.functions import load_functions
if st.session_state.logged_in:
  app = st.navigation(pages=load_functions())
else:
  app = st.navigation({"": [dashboard], "Account": [login_page, sign_up_page]})

app.run()
