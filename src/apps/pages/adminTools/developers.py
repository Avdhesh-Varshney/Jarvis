import streamlit as st
import requests

@st.cache_data
def fetchData():
	URL = "https://api.github.com/repos/Avdhesh-Varshney/Jarvis/contributors"
	data = {"UserName": [], "GitHub": [], "Avatar": [], "Contribution": []}
	response = requests.get(URL)
	if response.status_code == 200:
		for developer in response.json():
			data["UserName"].append(developer["login"])
			data["GitHub"].append(developer["html_url"])
			data["Avatar"].append(developer["avatar_url"])
			data["Contribution"].append(developer["contributions"])
	return data

def createCard(username, contribution, github, avatar_url):
	card_html = f"""
	<div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 10px; margin: 10px; width: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
		<img src="{avatar_url}" alt="{username}" style="border-radius: 50%; width: 150px; height: 150px; display: block; margin-left: auto; margin-right: auto;"/>
		<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
			<p style="font-size: 1.5rem;">@{username}</p>
			<p>Contribution: {contribution}</p>
			<p><a href="{github}" target="_blank">GitHub Profile</a></p>
		</div>
	</div>
	"""
	return card_html

def display_section(data):
	num_cols = 2
	num_items = len(data["UserName"])
	for i in range(0, num_items, num_cols):
		cols = st.columns(num_cols)
		for j in range(num_cols):
			if i + j < num_items:
				card_html = createCard(
					data["UserName"][i + j],
					data["Contribution"][i + j],
					data["GitHub"][i + j],
					data["Avatar"][i + j],
				)
				cols[j].markdown(card_html, unsafe_allow_html=True)
	st.markdown('---')

def developers():
	developersData = fetchData()
	Range = 1
	adminsData = {
		"UserName": developersData["UserName"][:Range],
		"GitHub": developersData["GitHub"][:Range],
		"Avatar": developersData["Avatar"][:Range],
		"Contribution": developersData["Contribution"][:Range],
	}

	contributorsData = {
		"UserName": developersData["UserName"][Range:],
		"GitHub": developersData["GitHub"][Range:],
		"Avatar": developersData["Avatar"][Range:],
		"Contribution": developersData["Contribution"][Range:],
	}

	st.header("😃 Project Admin")
	display_section(adminsData)

	st.subheader("💫 Our Valuable Contributors")
	display_section(contributorsData)

	st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis) if you like it!", icon='⭐')
	st.balloons()

developers()
