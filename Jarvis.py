from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from src.utils.functions import application
from src.emotion_recognition import run_emotion_detection  # Import emotion detection logic
from datetime import datetime, timedelta
import streamlit as st

# Initialize session state if not present
if "user" not in st.session_state:
    st.session_state.update({
        'password': None,
        'user': ['', '', '', '', '', '', '', ''],
        'expiration_date': (datetime.now() - timedelta(days=10)).isoformat(),
        'verified': False,
    })

# Function to fetch credentials from local storage
def get_credentials():
    conn = server()
    return (
        conn.getLocalStorageVal("password"),
        conn.getLocalStorageVal("user"),
        conn.getLocalStorageVal("expiration_date"),
        conn.getLocalStorageVal("verified"),
    )

# Main execution block
if __name__ == "__main__":
    today = datetime.now()

    # Fetch credentials from local storage if password is None
    if st.session_state['password'] is None:
        st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = get_credentials()

    # Check if the user's session is valid and not expired
    if st.session_state['expiration_date'] > today.isoformat() and not st.session_state['verified']:
        conn = create_connection()
        if login_user(conn, st.session_state['user'][0], st.session_state['password']):
            st.session_state['verified'] = True
            server().setLocalStorageVal("verified", True)

    # Run the application if the user is verified
    if st.session_state['verified']:
        # Optionally, run emotion detection here after user is verified
        run_emotion_detection()  # Trigger the emotion recognition (this could be interactive in the UI)

    # Run the application logic based on verified user status
    application(st.session_state['verified']).run()

