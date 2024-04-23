import streamlit as st
from database.sql import create_connection, create_usertable, login_user

st.set_option("client.showSidebarNavigation", True)

def login():
    st.sidebar.subheader("Login")
    text = st.sidebar.text_input("Username/Email:")
    password = st.sidebar.text_input("Password:", type="password")
    if st.sidebar.checkbox("Login"):
        conn = create_connection()
        create_usertable(conn)
        result = login_user(conn, text, password)
        if result:
            st.sidebar.success("Logged in as {}".format(result[0][3]), icon="✅")
            return [result[0][2], result[0][3]]
        else:
            st.sidebar.warning("Incorrect credentials!")
    return []

# login()
