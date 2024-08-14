import streamlit as st
import webbrowser as web
import requests

def myLocation():
  ip_add = requests.get('https://api.ipify.org').text
  url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
  geo_q = requests.get(url)
  geo_d = geo_q.json()

  city = geo_d['city']
  state = geo_d['region']
  country = geo_d['country']
  latitude = geo_d['latitude']
  longitude = geo_d['longitude']

  st.markdown(f"#### Currently, You are in {city}, {state}, {country}")
  if st.button("Show My Location"):
    st.write(f"Your Latitude is {latitude} and Longitude is {longitude}")
    url = f"https://www.google.com/maps/@?api=1&map_action=map&center={latitude}{longitude}"
    try:
      web.open(url)
    except:
      st.error("Website is not opening!!", icon="🚨")
