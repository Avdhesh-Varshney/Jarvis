import streamlit as st
import requests

def fetchData():
	URL = "https://api.github.com/repos/Avdhesh-Varshney/Jarvis/contributors"
	data = {"UserName": [], "GitHub": [], "Avatar": [], "Contribution": []}
	response = requests.get(URL)
	if response.status_code == 200:
		for contributor in response.json():
			data["UserName"].append(contributor["login"])
			data["GitHub"].append(contributor["html_url"])
			data["Avatar"].append(contributor["avatar_url"])
			data["Contribution"].append(contributor["contributions"])
	return data

def createCard(username, contribution, github, avatar_url):
	card_html = f"""
	<div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 10px; margin: 10px; width: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
		<img src="{avatar_url}" alt="{username}" style="border-radius: 50%; width: 150px; height: 150px; display: block; margin-left: auto; margin-right: auto;"/>
		<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
		<h4>@{username}</h4>
		<p>Contribution: {contribution}</p>
		<p><a href="{github}" target="_blank">GitHub Profile</a></p>
		</div>
	</div>
	"""
	return card_html

def contributors():
	st.title("💫 Our Valuable Contributors")
	contributorsData = fetchData()

	st.markdown('---')

	num_cols = 2
	num_contributors = len(contributorsData["UserName"])
	for i in range(0, num_contributors, num_cols):
		cols = st.columns(num_cols)
		for j in range(num_cols):
			if i + j < num_contributors:
				card_html = createCard(
				contributorsData["UserName"][i + j],
				contributorsData["Contribution"][i + j],
				contributorsData["GitHub"][i + j],
				contributorsData["Avatar"][i + j]
				)
				cols[j].markdown(card_html, unsafe_allow_html=True)

	st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis) if you like it!", icon='⭐')
	st.balloons()
