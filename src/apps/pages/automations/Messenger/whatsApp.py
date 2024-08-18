import streamlit as st
import pandas as pd
import pywhatkit
import pyautogui
import time

def whatsApp():
  st.markdown('### WhatsApp Automation 📨')
  st.write('This app sends a WhatsApp message to all the contacts in the CSV file.')

  csv_file = st.file_uploader('Upload your CSV file', type=['csv'])
  bottom = st.number_input('Enter the bottom range of phone numbers:', min_value=0, value=0)
  top = st.number_input('Enter the top range of phone numbers:', min_value=bottom+1, value=bottom+1)

  message = st.text_area('Enter the message to send:')

  if st.button('Send WhatsApp Message') and csv_file is not None:
    if message == '':
      st.warning('Please enter a message to send.', icon="⚠️")
      return
    
    df = pd.read_csv(csv_file)
    if top > len(df):
      st.warning('The top range of phone numbers exceeds the total number of phone numbers in the CSV file.', icon="⚠️")
      return

    if 'Phone Number' not in df.columns:
      st.warning('Please upload a CSV file with a column named "Phone Number".', icon="⚠️")
      return

    for index, row in df.iterrows():
      if index >= bottom and index < top:
        pywhatkit.sendwhatmsg_instantly(row['Phone Number'], message, wait_time=10)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'w')
        st.write(f'Message sent to {row["Phone Number"]}')
    st.write('All messages sent successfully!')
  else:
    st.info('Please upload a CSV file to send messages.', icon="ℹ️")
