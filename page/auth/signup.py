import streamlit as st
import os
from database.sql import valid_email, valid_username, create_connection, create_usertable, add_userdata, check_user

st.set_option("client.showSidebarNavigation", True)

def signup():
    st.subheader("Create New Account")
    new_name = st.text_input("Enter your name:")
    new_email = st.text_input("Enter your email:")
    x, y = st.columns(2)
    with x:
        new_gender = st.selectbox('Select your gender:', ['Male', 'Female'])
    with y:
        new_user = st.text_input("Create your username:")
    new_roles = st.selectbox("Select your role:", ["User", "Admin", "Super Admin"])
    new_age = st.slider('Enter your age:', 5, 80, 22)
    col1, col2 = st.columns(2)
    with col1:
        new_password = st.text_input("Enter password:", type='password')
    with col2:
        new_repeat_password = st.text_input('Re-type your password:', type='password')
    
    admin_key = os.environ.get("ADMIN_KEY")
    super_admin_key = os.environ.get("SUPER_ADMIN_KEY")

    if new_roles == 'Admin':
        pass_key = st.text_input('Enter your Admin key:')
        if pass_key != admin_key:
            st.warning("Invalid admin key!", icon="⚠️")
            return

    if new_roles == 'Super Admin':
        pass_key = st.text_input('Enter your Super admin key:')
        if pass_key != super_admin_key:
            st.warning("Invalid super admin key!", icon="⚠️")
            return

    if st.button("Signup"):
        if new_password == new_repeat_password:
            if valid_email(new_email):
                if valid_username(new_user):
                    conn = create_connection()
                    create_usertable(conn)
                    if check_user(conn, new_email) != None:
                        if check_user(conn, new_user) != None:
                            add_userdata(conn, new_user, new_name, new_roles, new_gender, new_age, new_email, new_password)
                            st.success("You have successfully created an valid account!", icon="✅")
                            st.info("Go to Login Menu to login!", icon="ℹ️")
                        else:
                            st.warning("Use different username!", icon="⚠️")
                    else:
                        st.warning("Use different email address!", icon="⚠️")
                else:
                    st.warning("Invalid username!", icon="⚠️")
            else:
                st.warning("Invalid email address!", icon="⚠️")
        else:
            st.warning("Password is not match!", icon="⚠️")

# signup()
