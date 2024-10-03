from database.localStorageServer import server
from datetime import datetime, timedelta
from src.auth.profile import profile
import streamlit as st

today = datetime.now()

def logout():
  if st.session_state['user'] != []:
    profile()
    if st.button("Log out"):
      conn = server()
      st.session_state["user"] = ['', '', '', '', '', '', '', '']
      conn.setLocalStorageVal("user", ['', '', '', '', '', '', '', ''])
      st.session_state['password'] = None
      conn.setLocalStorageVal("password", None)
      st.session_state['expiration_date'] = (today - timedelta(days=10)).isoformat()
      conn.setLocalStorageVal("expiration_date", (today - timedelta(days=10)).isoformat())
      st.session_state['verified'] = False
      conn.setLocalStorageVal("verified", False)
      st.info("Please refresh the page to continue", icon="ℹ️")
      st.rerun()

logout_page = st.Page(logout, title="My Profile", icon=":material/account_circle:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# /apps/public
home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

# /apps/pages/automations
websites = st.Page("src/apps/pages/automations/website.py", title="Websites", icon=":material/web:")
messenger = st.Page("src/apps/pages/automations/messenger.py", title="Messenger", icon=":material/email:")

# /apps/pages/models
chatBotModels = st.Page("src/apps/pages/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")
imageRecognizerModels = st.Page("src/apps/pages/models/imageRecognizerModel.py", title="Image Recognition Models", icon=":material/image_search:")
healthCareModels = st.Page("src/apps/pages/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")
objectDetectionModels = st.Page("src/apps/pages/models/objectDetectionModel.py", title="Object Detection Models", icon=":material/camera_alt:")
recommendationModels = st.Page("src/apps/pages/models/recommendationModel.py", title="Recommendation Models", icon=":material/recommend:")

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
    "": [home, youtubePlaylist],
    "Account": [logout_page],
    "Automations": [websites, messenger],
    "Models": [chatBotModels, imageRecognizerModels, healthCareModels, objectDetectionModels, recommendationModels],
    "Programs": [apiPrograms, games, imagePrograms, simplePrograms, studyPrograms],
  }
  user = st.session_state['user'].split(',')
  if user[4] == "Admin" or user[4] == "Super Admin":
    pages["Admin Tools"] = [contributors, packageUsed]
  
  if user[4] == "Super Admin":
    pages["Super Admin Controls"] = [userData]

  return pages
