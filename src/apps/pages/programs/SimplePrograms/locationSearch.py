import streamlit as st
import requests

def fetch_location_from_ip(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "success":
        return {
            "City": data.get("city", "N/A"),
            "Region": data.get("regionName", "N/A"),
            "Country": data.get("country", "N/A"),
            "Latitude": data.get("lat", "N/A"),
            "Longitude": data.get("lon", "N/A"),
            "ISP": data.get("isp", "N/A"),
        }
    return None

def locationSearch():
    st.title("🌍 IP Address to Location Lookup")

    ip_address = st.text_input("Enter an IP Address:")

    if st.button("Find Location"):
        with st.spinner("Fetching Location..."):
            location_info = fetch_location_from_ip(ip_address.strip())

        if location_info:
            st.subheader("📌 Location Details")
            st.write(f"**City:** {location_info['City']}")
            st.write(f"**Region:** {location_info['Region']}")
            st.write(f"**Country:** {location_info['Country']}")
            st.write(f"**Latitude:** {location_info['Latitude']}")
            st.write(f"**Longitude:** {location_info['Longitude']}")
            st.write(f"**ISP:** {location_info['ISP']}")
        else:
            st.error("❌ Could not fetch location. Try another IP!")
