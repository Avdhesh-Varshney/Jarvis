from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from datetime import datetime, timedelta
from src.auth.profile import profile
import streamlit as st
from scal import scientific_calculator  # Import your calculator function

today = datetime.now()

# Initialize session state variables
if "user" not in st.session_state:
    st.session_state['password'] = None
    st.session_state["user"] = ['', '', '', '', '', '', '', '']
    st.session_state['expiration_date'] = (today - timedelta(days=10)).isoformat()
    st.session_state['verified'] = False

def getCredentials():
    conn = server()
    return (
        conn.getLocalStorageVal("password"),
        conn.getLocalStorageVal("user"),
        conn.getLocalStorageVal("expiration_date"),
        conn.getLocalStorageVal("verified")
    )

def logged_in():
    from src.auth.login import login
    userData, password, remember_me = login()

    if userData != []:
        conn = server()
        user = [
            userData['username'],
            userData['email'],
            userData['first_name'],
            userData['last_name'],
            userData['role'],
            userData['gender'],
            userData['age'],
            userData['about']
        ]

        conn.setLocalStorageVal("user", user)
        conn.setLocalStorageVal("password", password)
        conn.setLocalStorageVal(
            "expiration_date",
            (today + timedelta(days=(30 if remember_me else 1))).isoformat()
        )
        conn.setLocalStorageVal("verified", True)
        st.info("Please refresh the page to continue", icon="ℹ️")

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

# Define pages for navigation
logout_page = st.Page(logout, title="My Profile", icon=":material/account_circle:")
login_page = st.Page(logged_in, title="Log in", icon=":material/login:")
sign_up_page = st.Page("src/auth/signup.py", title="Sign up", icon=":material/person_add:")

# Public Pages
home = st.Page("src/apps/public/home.py", title="Home", icon=":material/home:")
youtubePlaylist = st.Page("src/apps/public/youtubePlaylist.py", title="Jarvis Videos", icon=":material/ondemand_video:")

# Automation Pages
websites = st.Page("src/apps/pages/automations/website.py", title="Websites", icon=":material/web:")
messenger = st.Page("src/apps/pages/automations/messenger.py", title="Messenger", icon=":material/email:")

# Model Pages
chatBotModels = st.Page("src/apps/pages/models/chatBotModel.py", title="Chat Bot Models", icon=":material/smart_toy:")
healthCareModels = st.Page("src/apps/pages/models/healthCareModel.py", title="Health Care Models", icon=":material/health_and_safety:")
objectDetectionModels = st.Page("src/apps/pages/models/objectDetectionModel.py", title="Object Detection Models", icon=":material/camera_alt:")
recommendationModels = st.Page("src/apps/pages/models/recommendationModel.py", title="Recommendation Models", icon=":material/recommend:")

# Program Pages
simplePrograms = st.Page("src/apps/pages/programs/simpleProgram.py", title="Simple Programs", icon=":material/emoji_objects:")
apiPrograms = st.Page("src/apps/pages/programs/apiProgram.py", title="API Programs", icon=":material/api:")
imagePrograms = st.Page("src/apps/pages/programs/imageProgram.py", title="Image Programs", icon=":material/image:")
games = st.Page("src/apps/pages/programs/games.py", title="Games", icon=":material/casino:")
studyPrograms = st.Page("src/apps/pages/programs/studyProgram.py", title="Study Programs", icon=":material/school:")

# Admin Tool Pages
contributors = st.Page("src/apps/pages/adminTools/contributors.py", title="Contributors", icon=":material/people:")
packageUsed = st.Page("src/apps/pages/adminTools/packageUsed.py", title="Package Used", icon=":material/extension:")

# Super Admin Control Pages
userData = st.Page("src/apps/pages/superAdminControls/userData.py", title="Users Data", icon=":material/data_usage:")

# Calculator Page
calculator_page = st.Page(scientific_calculator, title="Calculator", icon="🔢")

def load_functions():
    pages = {
        "": [home, youtubePlaylist],
        "Account": [logout_page],
        "Automations": [websites, messenger],
        "Models": [chatBotModels, healthCareModels, objectDetectionModels, recommendationModels],
        "Programs": [apiPrograms, games, imagePrograms, simplePrograms, studyPrograms],
        "Tools": [calculator_page],  # Add the calculator here
    }
    user = st.session_state['user']
    if user[4] == "Admin" or user[4] == "Super Admin":
        pages["Admin Tools"] = [contributors, packageUsed]
    
    if user[4] == "Super Admin":
        pages["Super Admin Controls"] = [userData]
    
    return pages

if __name__ == "__main__":
    # Initialize the application
    if st.session_state['password'] is None:
        (
            st.session_state['password'],
            st.session_state['user'],
            st.session_state['expiration_date'],
            st.session_state['verified']
        ) = getCredentials()

    if st.session_state['password'] is not None and st.session_state['expiration_date'] > today.isoformat():
        if not st.session_state['verified']:
            conn = create_connection()
            result = login_user(conn, st.session_state['user'][0], st.session_state['password'])
            if result:
                st.session_state['verified'] = True
                conn = server()
                conn.setLocalStorageVal("verified", True)
        if st.session_state['verified']:
            # Load authenticated pages
            app = st.navigation(pages=load_functions())
    else:
        # Load public pages
        app = st.navigation(pages=load_functions())

    app.run()
