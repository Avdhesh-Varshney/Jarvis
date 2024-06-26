import streamlit as st
from src.auth.profile import profile

def logout():
  if st.session_state.logged_in:
    profile()
    if st.button("Log out"):
      st.session_state.logged_in = False
      st.rerun()

logout_page = st.Page(logout, title="My Profile", icon=":material/account_circle:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# /apps
dashboard = st.Page("src/apps/dashboard.py", title="Dashboard", icon=":material/dashboard:")

# /apps/pages/models/healthCareModels
healthCareModels = st.Page("src/apps/pages/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")
chatBotModels = st.Page("src/apps/pages/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")

# /apps/pages/programs/casualPrograms
casualPrograms = st.Page("src/apps/pages/programs/casualProgram.py", title="Casual Programs", icon=":material/emoji_objects:")

def load_functions():
  pages = {
    "": [dashboard],
    "Account": [logout_page],
    "Models": [healthCareModels, chatBotModels],
    "Programs": [casualPrograms],
  }

  return pages
