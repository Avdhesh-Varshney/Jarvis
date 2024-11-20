from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from src.utils.functions import application
from datetime import datetime, timedelta
import streamlit as st

if "user" not in st.session_state:
    st.session_state.update({
        'password': None,
        'user': ['', '', '', '', '', '', '', ''],
        'expiration_date': (datetime.now() - timedelta(days=10)).isoformat(),
        'verified': False,
    })

def get_credentials():
    conn = server()
    return (
        conn.getLocalStorageVal("password"),
        conn.getLocalStorageVal("user"),
        conn.getLocalStorageVal("expiration_date"),
        conn.getLocalStorageVal("verified"),
    )

if __name__ == "__main__":
    today = datetime.now()

    if st.session_state['password'] is None:
        st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = get_credentials()

    if st.session_state['expiration_date'] > today.isoformat() and not st.session_state['verified']:
        conn = create_connection()
        if login_user(conn, st.session_state['user'][0], st.session_state['password']):
            st.session_state['verified'] = True
            server().setLocalStorageVal("verified", True)

    application(st.session_state['verified']).run()
