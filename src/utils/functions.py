from datetime import datetime, timedelta
import streamlit as st

today = datetime.now()

def logged_in():
  from src.auth.login import login
  userData, password, remember_me = login()

  if userData != []:
    from database.localStorageServer import server
    conn = server()
    user = [userData['username'], userData['email'], userData['first_name'], userData['last_name'], userData['role'], userData['gender'], userData['age'], userData['about']]

    conn.setLocalStorageVal("user", user)
    conn.setLocalStorageVal("password", password)
    conn.setLocalStorageVal("expiration_date", (today + timedelta(days=(30 if remember_me else 1))).isoformat())
    conn.setLocalStorageVal("verified", True)
    st.info("Please refresh the page to continue", icon="ℹ️")
    st.rerun()

# /auth
login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
logout_page = st.Page("src/auth/profile.py", title="My Profile", icon=":material/account_circle:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# /apps/public
home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

# /apps/pages/automations
coding = st.Page("src/apps/pages/automations/coding.py", title="Coding Platforms", icon=":material/code:")
websites = st.Page("src/apps/pages/automations/website.py", title="Websites", icon=":material/web:")
socialMediaApps = st.Page("src/apps/pages/automations/socialMediaApps.py", title="Social Media Apps", icon=":material/share:")
messenger = st.Page("src/apps/pages/automations/messenger.py", title="Messenger", icon=":material/email:")

# /apps/pages/models
chatBotModels = st.Page("src/apps/pages/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")
healthCareModels = st.Page("src/apps/pages/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")
objectDetectionModels = st.Page("src/apps/pages/models/objectDetectionModel.py", title="Object Detection Models", icon=":material/camera_alt:")
recommendationModels = st.Page("src/apps/pages/models/recommendationModel.py", title="Recommendation Models", icon=":material/recommend:")

# /apps/pages/programs
simplePrograms = st.Page("src/apps/pages/programs/simpleProgram.py", title="Simple Programs", icon=":material/emoji_objects:")
apiPrograms = st.Page("src/apps/pages/programs/apiProgram.py", title="API Programs", icon=":material/api:")
imagePrograms = st.Page("src/apps/pages/programs/imageProgram.py", title="Image Programs", icon=":material/image:")
games = st.Page("src/apps/pages/programs/games.py",title="Games",icon=":material/casino:")
studyPrograms = st.Page("src/apps/pages/programs/studyProgram.py", title="Study Programs", icon=":material/school:")

# /apps/pages/adminTools
developers = st.Page("src/apps/pages/adminTools/developers.py", title="Developers", icon=":material/people:")
packageUsed = st.Page("src/apps/pages/adminTools/packageUsed.py", title="Package Used", icon=":material/extension:")

# /apps/pages/superAdminControls
userData = st.Page("src/apps/pages/superAdminControls/userData.py", title="Users Data", icon=":material/data_usage:")

def application(verified):
  if verified == "true":
    pages = {
      "": [home, youtubePlaylist],
      "Account": [logout_page],
      "Automations": [coding, websites, socialMediaApps, messenger],
      "Models": [chatBotModels, healthCareModels, objectDetectionModels, recommendationModels],
      "Programs": [apiPrograms, games, imagePrograms, simplePrograms, studyPrograms],
    }
    user = st.session_state['user'].split(',')
    if user[4] == "Admin" or user[4] == "Super Admin":
      pages["Admin Tools"] = [developers, packageUsed]
    
    if user[4] == "Super Admin":
      pages["Super Admin Controls"] = [userData]
    return st.navigation(pages)

  return st.navigation({"": [home, youtubePlaylist], "Account": [login_page, sign_up_page]})
