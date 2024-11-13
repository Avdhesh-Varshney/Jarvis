from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from src.apps.page import application
from datetime import datetime, timedelta
import streamlit as st

today = datetime.now()

if "user" not in st.session_state:
	st.session_state['password'] = None
	st.session_state["user"] = ['', '', '', '', '', '', '', '']
	st.session_state['expiration_date'] = (today - timedelta(days=10)).isoformat()
	st.session_state['verified'] = False

def getCredentials():
	conn = server()
	return conn.getLocalStorageVal("password"), conn.getLocalStorageVal("user"), conn.getLocalStorageVal("expiration_date"), conn.getLocalStorageVal("verified")

if __name__ == "__main__":
	app = application()

	if st.session_state['password'] is None:
		st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = getCredentials()

	if st.session_state['password'] is not None and st.session_state['expiration_date'] > today.isoformat():
		if not st.session_state['verified']:
			conn = create_connection()
			result = login_user(conn, st.session_state['user'].split(',')[0], st.session_state['password'])
			if result:
				st.session_state['verified'] = True
				conn = server()
				conn.setLocalStorageVal("verified", True)
				st.rerun()
			st.rerun()
