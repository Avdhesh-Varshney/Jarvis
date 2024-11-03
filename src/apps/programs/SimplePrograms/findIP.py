import streamlit as st
import streamlit.components.v1 as components

def fetch_ip_address(url, ip_type):
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
        fetch('{url}')
        .then(response => response.json())
        .then(data => {{
            document.getElementById("ip_display").innerText = data.ip;
        }})
        .catch(err => {{
            console.error("Error fetching IP:", err);
            document.getElementById("ip_display").innerText = "Failed to fetch IP.";
        }});
    </script>
    <div style="border:none; width:300px; display:flex; align-items:center; height: 20px;">
        <p style="font-size:20px; color:#FFFFFF; margin-right:10px;">{ip_type}: </p>
        <p id="ip_display" style="font-size:20px; color:#32ca5b;">Fetching IP...</p>
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


def findIP():
    st.title("Your Public IP Address")

    ipv4 = fetch_ip_address('https://api.ipify.org?format=json', 'IPV4')
    components.html(ipv4, height=40)

    ipv6 = fetch_ip_address('https://api64.ipify.org?format=json', 'IPV6')
    components.html(ipv6, height=40)