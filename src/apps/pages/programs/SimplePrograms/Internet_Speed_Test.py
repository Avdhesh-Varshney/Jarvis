# A simple program to test speed of internet
import streamlit as st
import speedtest

# Creating the function for the app
def Internet_Speed_Test():
    def int_st(choice):
        sp_test = speedtest.Speedtest()  
        sp_test.get_best_server()
        if choice == "Download Speed":
            return sp_test.download() / 1000000  # Converting speed from bps to mbps
        elif choice == "Upload Speed":
            return sp_test.upload() / 1000000
        elif choice == "Ping":
            return sp_test.results.ping  # in milliseconds
        else:
            st.error("Invalid choice")
            return None
    
    # Streamlit app code
    st.title("INTERNET SPEED TEST")
    with st.form("Int_st form"):
        choice = st.selectbox("Choose the Speed test type", ["Download Speed", "Upload Speed", "Ping"])
        submitted = st.form_submit_button("Run Speed Test")
        if submitted:
            res = int_st(choice)
            if res is not None:
                if choice == "Download Speed":
                    st.write(f"Download Speed: {res:.2f} Mbps")
                elif choice == "Upload Speed":
                    st.write(f"Upload Speed: {res:.2f} Mbps")
                elif choice == "Ping":
                    st.write(f"Ping: {res:.2f} ms")



