import streamlit as st
import sys
import numpy as np

# core files
from page.functions import load_functions

# code files
sys.path.insert(1, './source/')
from source.basicFunctions.English import Speak
from source.features.healthcarePrograms.diabetes_test import diabetesTestForm,do_diabetes_test
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

    st.write(data[0])
    #  CODE to greet User on Login
    if 'greet' not in st.session_state:
        st.session_state.greet = False
        from source.basicFunctions.Greeting import GreetUser
        Speak(f"{GreetUser(data[0])}, It's Jarvis...")
        Speak("Login Successfully!")
        st.session_state.greet = True         

    choice = st.selectbox('Services:', service_list)
    
    if choice != None:
        main_list = [None] + list(functions[choice])[0]
        choice2 = st.selectbox('Programs:', main_list)

    # Here is the HealthCare Programs
    if choice == "Healthcare Programs":
        if choice2 == "Diabetes Test":
            st.write("Enter all details for better results")
            diabetes_testset,db_btn = diabetesTestForm()
            diabetes_testset = np.array(diabetes_testset)
            diabetes_testset = diabetes_testset.reshape(-1,7)
            diabetes_res = do_diabetes_test(diabetes_testset)
            if db_btn== True :
                if diabetes_res == 0:
                    st.success(f'Congrats {data[0]},\n You are not diagnosed with diabetes')
                if diabetes_res==1:
                    st.error(f'Hi {data[0]},\nYou are diagnosed with diabetes.\nPlease consult a doctor.')
    else:
        st.info(f"Hello {data[0]}, Start your work!", icon="ℹ️")
