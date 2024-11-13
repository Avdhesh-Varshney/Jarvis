import streamlit as st

def userData():
	st.title("📦 Users Data")
	key = st.text_input("Enter the Admin key", type="password")
	if st.button("Show Data") and key == st.secrets["ADMIN_KEY"]:
		from database.mongodb import show_data
		data = show_data()
		st.dataframe(data)
	else:
		st.info("Provide the correct key to view the data", icon="ℹ️")
