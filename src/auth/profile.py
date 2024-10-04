import streamlit as st
from PIL import Image

def profile():
  st.title("👤 Profile Page")

  user = st.session_state['user'].split(',')
  col1, col2 = st.columns([1, 3])
  with col1:
    if user[5] == 'Male':
      image = Image.open("assets/boy.webp")
    else:
      image = Image.open("assets/girl.jpg")
    st.image(image, width=100)
  with col2:
    st.write(f"**Name:** {user[2]} {user[3]}")
    st.write(f"**Username:** @{user[0]}")

  st.markdown("---")
  
  # User details section
  st.write("### User Details")
  
  col3, col4 = st.columns(2)
  with col3:
    st.write(f"**🛠 Role:** {user[4]}")
    st.write(f"**🎂 Age:** {user[6]}")
  with col4:
    st.write(f"**⚥ Gender:** {user[5]}")
    st.write(f"**📧 Email:** {user[1]}")
  
  st.markdown("---")
  
  # Adding some fun elements
  st.markdown("### About Me")
  st.write(user[7:][0])
