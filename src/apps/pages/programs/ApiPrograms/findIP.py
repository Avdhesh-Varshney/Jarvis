import streamlit as st
import requests

def findIP():
  ip_address = requests.get('https://api64.ipify.org?format=json').json()
  st.write(f"Your IP Address is: {ip_address['ip']}")
