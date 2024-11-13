import streamlit as st
import requests
import os

def getWeather(api_key, city):
	try:
		url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
		response = requests.get(url)
		data = response.json()
		if response.status_code == 200:
			weather = {
				"city": data["location"]["name"],
				"country": data["location"]["country"],
				"temperature": data["current"]["temp_c"],
				"humidity": data["current"]["humidity"],
				"pressure": data["current"]["pressure_mb"],
				"wind_speed": data["current"]["wind_kph"],
				"condition": data["current"]["condition"]["text"],
				"icon": data["current"]["condition"]["icon"],
				"feels_like": data["current"]["feelslike_c"],
				"last_updated": data["current"]["last_updated"]
			}
			return weather, None
		else:
			return None, data.get("error", {}).get("message", "Unknown error")
	except Exception as e:
		return None, str(e)

def API_Exists():
	if "WEATHER_API_KEY" in st.secrets['api_key'] and st.secrets['api_key']["WEATHER_API_KEY"]:
		return True
	elif "WEATHER_API_KEY" in os.environ and os.environ["WEATHER_API_KEY"]:
		return True
	return False

def showInstructions():
	st.markdown("### Weather App")
	st.markdown("""### How to get your API Key:
	1. Visit [WeatherAPI.com](https://www.weatherapi.com/).
	2. Sign up for a free account.
	3. Generate an API key from your account dashboard.
	4. Enter the API key in the input field.
	""")
	api_key = st.text_input("Enter your WeatherAPI.com API Key")
	if st.button("Enter") and api_key != "":
		os.environ["WEATHER_API_KEY"] = api_key
		st.rerun()

def weatherApp():
	if API_Exists():
		api_key = (os.environ.get("WEATHER_API_KEY") or st.secrets['api_key']["WEATHER_API_KEY"])
		st.markdown("### Weather App")
		city = st.text_input("Enter City Name")

		if st.button("Get Weather"):
			if api_key and city:
				weather, error = getWeather(api_key, city)
				if weather:
					st.subheader(f"Weather in {weather['city']}, {weather['country']}")
					col1, col2 = st.columns(2)
					with col1:
						st.image(f"http:{weather['icon']}")
						st.write(f"**{weather['condition']}**")
					with col2:
						st.write(f"**Temperature:** {weather['temperature']} °C")
						st.write(f"**Feels Like:** {weather['feels_like']} °C")
						st.write(f"**Humidity:** {weather['humidity']} %")
						st.write(f"**Pressure:** {weather['pressure']} hPa")
						st.write(f"**Wind Speed:** {weather['wind_speed']} kph")
					st.write(f"**Last Updated:** {weather['last_updated']}")
				else:
					st.error(f"Error: {error}")
			else:
				st.error("Please provide both API Key and City Name.")
	else:
		showInstructions()
