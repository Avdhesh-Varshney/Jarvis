from datetime import datetime
import pytz
import streamlit as st
import time

def get_city_time(timezone):
    tz = pytz.timezone(timezone)
    city_time = datetime.now(tz)
    return city_time.strftime('%H:%M:%S'), city_time.strftime('%A, %Y-%m-%d')

def worldClock():
    st.title("World Clock")

    cities = {
        "New York": "America/New_York",
        "London": "Europe/London",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney",
        "Delhi": "Asia/Kolkata",
        "Paris": "Europe/Paris"
    }

    selected_city = st.selectbox("Select a city", list(cities.keys()))

    if selected_city:
        time_placeholder = st.empty()
        date_placeholder = st.empty()

        while True:
            city_time, city_date = get_city_time(cities[selected_city])
            time_placeholder.markdown(f"# {city_time}")
            date_placeholder.markdown(f"## {city_date}")
            time.sleep(1)
