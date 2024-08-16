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

# /apps/public
dashboard = st.Page("src/apps/public/dashboard.py", title="Dashboard", icon=":material/dashboard:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

# /apps/pages/automations
websites = st.Page("src/apps/pages/automations/website.py", title="Websites", icon=":material/web:")

# /apps/pages/models
chatBotModels = st.Page("src/apps/pages/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")
healthCareModels = st.Page("src/apps/pages/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")

# /apps/pages/programs
simplePrograms = st.Page("src/apps/pages/programs/simpleProgram.py", title="Simple Programs", icon=":material/emoji_objects:")
apiPrograms = st.Page("src/apps/pages/programs/apiProgram.py", title="API Programs", icon=":material/api:")
imagePrograms = st.Page("src/apps/pages/programs/imageProgram.py", title="Image Programs", icon=":material/image:")
games = st.Page("src/apps/pages/programs/games.py",title="Games",icon=":material/casino:")
studyPrograms = st.Page("src/apps/pages/programs/studyProgram.py", title="Study Programs", icon=":material/school:")

# /apps/pages/adminTools/contributors
contributors = st.Page("src/apps/pages/adminTools/contributors.py", title="Contributors", icon=":material/people:")
packageUsed = st.Page("src/apps/pages/adminTools/packageUsed.py", title="Package Used", icon=":material/extension:")

# /apps/pages/superAdminControls/userData
userData = st.Page("src/apps/pages/superAdminControls/userData.py", title="Users Data", icon=":material/data_usage:")

def load_functions():
  pages = {
    "": [dashboard, youtubePlaylist],
    "Account": [logout_page],
    "Automations": [websites],
    "Models": [chatBotModels, healthCareModels],
    "Programs": [apiPrograms, games, imagePrograms, simplePrograms, studyPrograms],
  }

  if st.session_state.user["role"] == "Admin" or st.session_state.user["role"] == "Super Admin":
    pages["Admin Tools"] = [contributors, packageUsed]
  
  if st.session_state.user["role"] == "Super Admin":
    pages["Super Admin Controls"] = [userData]

  return pages
