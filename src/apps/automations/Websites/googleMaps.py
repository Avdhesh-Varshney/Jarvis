import streamlit as st
import webbrowser as web
import geocoder
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

def googleMaps():
	st.markdown("#### Welcome To Google Maps Automation")
	try:
		count = 1
		while(count > 0):
			count = count - 1
			# st.write("Sir, How Can I Help You?")
			# query = ListenInEnglish()
			query = '281'

			# if 'exit' or 'leave' or 'close' in query:
			#     break

			query = query.replace("jarvis","")
			query = query.replace("open google maps","")
			query = query.replace("google maps automation","")
			query = query.replace("google maps automations","")
			query = query.replace("google maps","")
			query = query.replace("","")

			Place = str(query).lower()

			url_Place = "https://www.google.com/maps/place/" + str(Place)
			web.open(url=url_Place)

			geolocator = Nominatim(user_agent="myGeocoder")
			location = geolocator.geocode(Place,addressdetails= True)
			target_latlon = location.latitude, location.longitude
			location = location.raw['address']
			print(location)

			target = {'city' : location.get('city',''),
								'district' : location.get('city_district',''),
								'state' : location.get('state',''),
								'country' : location.get('country','')}

			current_loca = geocoder.ip('me')
			current_larlon = current_loca.latlng

			distance = str(great_circle(current_larlon,target_latlon))
			distance = str(distance.split(' ', 1)[0])
			distance = round(float(distance),2)

			st.write(target)
			st.write(f"Sir, {Place} is {distance} kilometre away from Your Location.")

	except:
		st.write("Sorry Sir, Operation Cannot be done!!")
