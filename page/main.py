import streamlit as st
import sys

# core files
from page.functions import load_functions


# code files
sys.path.insert(1, './source/')
from source.Basic_Functions.English import Speak

st.set_option("client.showSidebarNavigation", True)

def main(data):
    st.write(f'Welcome back, *{data[1]}*')
    functions = load_functions()

    service_list = [None] + list(functions.keys())
    
    if data[1] == 'Admin' and 'Super Admin Programs' in service_list:
        service_list.remove('Super Admin Programs')
    elif data[1] == 'User':
        if 'Super Admin Programs' in service_list:
            service_list.remove('Super Admin Programs')
        if 'Admin Programs' in service_list:
            service_list.remove('Admin Programs')

    choice = st.selectbox('Services:', service_list)
    if choice != None:
        main_list = [None] + list(functions[choice])[0]
        choice2 = st.selectbox('Programs:', main_list)
        
        if choice2 != None:
            from source.Basic_Functions.Greeting import GreetUser
            Speak(f"{GreetUser()}, It's Jarvis...")
            Speak("Login Successfully!")
    else:
        st.info(f"Hello {data[0]}, Start your work!", icon="ℹ️")
    
if __name__ == '__main__':
    # Sample user data for testing
    sample_data = ("User", "Admin")  # replace this with actual data fetching logic
    main(sample_data)
