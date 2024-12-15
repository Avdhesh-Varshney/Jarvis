import requests
from local_ip import get_local_ip  # Import your function to get the local IP

def get_public_ip():
    """Fetch your public IP address using ipify"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text  # Return the public IP address
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def get_location_from_ip(ip_address):
    """Fetch location data using ipinfo.io API"""
    url = f'https://ipinfo.io/{ip_address}/json'

    try:
        # Send GET request to ipinfo.io API
        response = requests.get(url)
        data = response.json()

        # Check if the response is successful
        if response.status_code == 200:
            location_info = {
                "IP": ip_address,
                "City": data.get("city"),
                "Region": data.get("region"),
                "Country": data.get("country"),
                "Org":data.get("org"),
                "Location (Latitude, Longitude)": data.get("loc"),
                "Postal Code": data.get("postal"),
                "Timezone": data.get("timezone")
            }
            return location_info
        else:
            return f"Error: Unable to fetch location data. API returned status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Fetch the public IP address
public_ip = get_public_ip()

# Use the public IP to fetch location data
location = get_location_from_ip(public_ip)
print("Public IP:", public_ip)
print("Location Info:", location)