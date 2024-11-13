import streamlit as st
import requests
import webbrowser as web
import streamlit.components.v1 as components

# Function to fetch geolocation from the IP address
def get_geolocation(ip):
    geo_url = f'https://get.geojs.io/v1/ip/geo/{ip}.json'
    geo_q = requests.get(geo_url)
    if geo_q.status_code == 200:
        geo_d = geo_q.json()
        return geo_d
    else:
        st.error('Invalid IP address')

# fetch dns pointer of IP
def get_dns_ptr(ip):
    dns = f'https://get.geojs.io/v1/dns/ptr/{ip}.json'
    dns_q = requests.get(dns)
    if dns_q.status_code == 200:
        dns_d = dns_q.json()
        return dns_d
    else:
        st.error('Invalid IP address')


def fetch_ip_address():
    ip_script = f"""
    <style> 
        .styled-button {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }}
        .styled-button:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}
    </style>
    <script>
        fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {{
            document.getElementById("ip_display").innerText = data.ip;
        }})
        .catch(err => {{
            console.error("Error fetching IP:", err);
            document.getElementById("ip_display").innerText = "Failed to fetch IP.";
        }});
    </script>
    <div style="border:none; width:300px; display:flex; align-items:center; height: 20px;" >
        <p style="font-size:18px; color:#FFFFFF; margin-right:5px;">My IP:</p>
        <p id="ip_display" style="font-size:18px; color:#32ca5b;">Fetching IP...</p>
        <button class="styled-button" id="styled-button" onclick="copyIP()">Copy</button>
    </div>
    <script>
        function copyIP() {{
            document.getElementById("styled-button").innerText = 'Copied';
            let ip = document.getElementById("ip_display").innerText;
            navigator.clipboard.writeText(ip);
            setTimeout(() => {{
                document.getElementById("styled-button").innerText = 'Copy';
            }}, 1000);
        }}
    </script>
    """
    return ip_script


def format(data):
    return f'<span style="font-size:19px; color:#32ca5b;">{data}</span>'


def myLocation():

    components.html(fetch_ip_address(), height=40)

    ip_address = st.text_input("Enter IP address:", placeholder='Enter IP...')

    if ip_address:
        geo = get_geolocation(ip_address)
        if geo:
            st.markdown(f"""The IP address {format(geo['ip'])} is located in {format(geo.get('city', '-'))}, 
                        {format(geo.get('region', '-'))}, {format(geo.get('country', '-'))}, continent {format(geo.get('continent_code', '-'))} 
                        with coordinates at latitude {format(geo.get('latitude', '-'))} and longitude {format(geo.get('longitude', '-'))} 
                        within a radius of {format(geo.get('accuracy', '-'))} kms.
                    The associated timezone is {format(geo.get('timezone', '-'))}.
                     """, unsafe_allow_html=True)
            st.markdown(f"""The organization this IP is registered to is "{format(geo.get('organization_name', '-'))}". The asn 
                        (autonomous number system) associated with it is {format(geo.get('asn', '-'))}.
                     """, unsafe_allow_html=True)

            if st.button("Show Location"):
                maps_url = f"https://www.google.com/maps/@?api=1&map_action=map&center={geo.get('latitude','-')},{geo.get('longitude', '-')}"
                try:
                    web.open(maps_url)
                except:
                    st.error("Website is not opening!!", icon="🚨")

        dns_ptr = get_dns_ptr(ip_address)
        if dns_ptr and dns_ptr['ptr']!="Failed to get PTR record":
            st.markdown(f"DNS pointer record this IP is {format(dns_ptr.get('ptr', '-'))}.", unsafe_allow_html=True)
