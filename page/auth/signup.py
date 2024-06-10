from page.auth.encrypt import check_password, secure_password
import streamlit as st
import os
from database.sql import valid_email, valid_username, create_connection, create_usertable, add_userdata, check_user

st.set_option("client.showSidebarNavigation", True)

def signup():
    st.title("Signup Form")
    st.subheader("Create a New Account")
    st.markdown("Please fill out the form below to create a new account.")

    st.markdown("## Personal Information")
    new_name = st.text_input("👤 Enter your name:")
    new_email = st.text_input("📧 Enter your email:")

    st.markdown("## Account Details")
    new_user = st.text_input("👥 Create your username:")

    col1, col2 = st.columns(2)
    with col1:
        new_gender = st.radio('⚧ Select your gender:', ['Male', 'Female', 'Other'])
    with col2:
        new_roles = st.selectbox("👔 Select your role:", ["User", "Admin", "Super Admin"])

    new_age = st.slider('🎂 Enter your age:', 5, 80, 22)

    st.markdown("## Password")
    col3, col4 = st.columns(2)
    with col3:
        new_password = str(st.text_input("🔑 Enter password:", type='password'))
        new_password_hashed = secure_password(new_password)
    with col4:
        new_repeat_password = str(st.text_input('🔑 Re-type your password:', type='password'))

    admin_key = os.environ.get("ADMIN_KEY")
    super_admin_key = os.environ.get("SUPER_ADMIN_KEY")

    if new_roles == 'Admin':
        pass_key = st.text_input('🔑 Enter your Admin key:')
        if pass_key != admin_key:
            st.warning("Invalid admin key!", icon="⚠️")
            return

    if new_roles == 'Super Admin':
        pass_key = st.text_input('🔑 Enter your Super admin key:')
        if pass_key != super_admin_key:
            st.warning("Invalid super admin key!", icon="⚠️")
            return

    st.markdown("---")
    if st.button("Signup"):
        if check_password(new_repeat_password, new_password_hashed):
            if valid_email(new_email):
                if valid_username(new_user):
                    conn = create_connection()
                    create_usertable(conn)
                    if check_user(conn, new_email) != None:
                        if check_user(conn, new_user) != None:
                            add_userdata(conn, new_user, new_name, new_roles, new_gender, new_age, new_email, new_password)
                            st.success("You have successfully created a valid account!", icon="✅")
                            st.info("Go to Login Menu to login!", icon="ℹ️")
                        else:
                            st.warning("Use a different username!", icon="⚠️")
                    else:
                        st.warning("Use a different email address!", icon="⚠️")
                else:
                    st.warning("Invalid username!", icon="⚠️")
            else:
                st.warning("Invalid email address!", icon="⚠️")
        else:
            st.warning("Passwords do not match!", icon="⚠️")

if __name__ == "__main__":
    signup()
