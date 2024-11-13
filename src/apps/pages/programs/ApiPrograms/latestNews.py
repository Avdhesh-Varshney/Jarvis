import streamlit as st
import requests
import os
from datetime import datetime

COUNTRIES = {
	"United Arab Emirates": "AE",
	"Argentina": "AR",
	"Austria": "AT",
	"Australia": "AU",
	"Belgium": "BE",
	"Bulgaria": "BG",
	"Brazil": "BR",
	"Canada": "CA",
	"Switzerland": "CH",
	"China": "CN",
	"Colombia": "CO",
	"Cuba": "CU",
	"Czech Republic": "CZ",
	"Germany": "DE",
	"Egypt": "EG",
	"France": "FR",
	"United Kingdom": "GB",
	"Greece": "GR",
	"Hong Kong": "HK",
	"Hungary": "HU",
	"Indonesia": "ID",
	"Ireland": "IE",
	"Israel": "IL",
	"India": "IN",
	"Italy": "IT",
	"Japan": "JP",
	"South Korea": "KR",
	"Lithuania": "LT",
	"Latvia": "LV",
	"Morocco": "MA",
	"Mexico": "MX",
	"Malaysia": "MY",
	"Nigeria": "NG",
	"Netherlands": "NL",
	"New Zealand": "NZ",
	"Philippines": "PH",
	"Poland": "PL",
	"Portugal": "PT",
	"Romania": "RO",
	"Russia": "RU",
	"Saudi Arabia": "SA",
	"Sweden": "SE",
	"Singapore": "SG",
	"Slovakia": "SK",
	"Thailand": "TH",
	"Turkey": "TR",
	"Taiwan": "TW",
	"Ukraine": "UA",
	"United States": "US",
	"Venezuela": "VE",
	"South Africa": "ZA"
}

CATEGORIES = {
	"Business": "business",
	"Entertainment": "entertainment",
	"General": "general",
	"Health": "health",
	"Science": "science",
	"Sports": "sports",
	"Technology": "technology"
}

REQUIRED = {
	"Top Headlines": "top-headlines",
	"Everything": "everything"
}

SORTBY = {
	"Published At": "publishedAt",
	"Relevancy": "relevancy",
	"Popularity": "popularity"
}

def API_Exists():
	if "NEWS_API_KEY" in st.secrets['api_key'] and st.secrets['api_key']["NEWS_API_KEY"]:
		return True
	elif "NEWS_API_KEY" in os.environ and os.environ["NEWS_API_KEY"]:
		return True
	return False

def showInstructions():
	st.markdown("""### How to get your API Key:
	1. Visit [newsapi.org](https://newsapi.org/).
	2. Sign up for a free account.
	3. Generate an API key from your account dashboard.
	4. Enter the API key in the input field.
	""")
	api_key = st.text_input("Enter your newsapi.org API Key")
	if st.button("Enter") and api_key != "":
		os.environ["NEWS_API_KEY"] = api_key
		st.rerun()

def formatISODate(iso_date_str):
	dateObj = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%SZ")
	date = dateObj.strftime("%B %d, %Y, %I:%M %p")
	return date

# TODO: Show more headlines of next page on button click
def showHeadlines(API, required, country, category):
	news_headlines = []
	URL = f'https://newsapi.org/v2/{REQUIRED[required]}?country={COUNTRIES[country].lower()}&apiKey={API}&category={CATEGORIES[category]}'
	try:
		response = requests.get(URL)
		data = response.json()
		if response.status_code == 200:
			articles = data["articles"]
			for article in articles:
				news_headlines.append(article["title"])

			for i in range(len(news_headlines)):
				st.markdown(f"##### {i+1} - {news_headlines[i]}")
				st.write("\n")
	except Exception as e:
		st.error(str(e))

def showNews(API, required, query, sortby):
	URL = f'https://newsapi.org/v2/{REQUIRED[required]}?q={query}&sortBy={SORTBY[sortby]}&apiKey={API}'
	try:
		response = requests.get(URL)
		data = response.json()
		if response.status_code == 200:
			articles = data["articles"]
			for article in articles:
				if article['urlToImage']:
					st.image(article['urlToImage'], caption=article['title'])
				else:
					st.write(article['title'])
				
				col1, col2, col3 = st.columns(3)
				with col1:
					st.write(f"Author: {article['author']}")
				with col2:
					st.write(f"Source: {article['source']['name']}")
				with col3:
					st.write(f"{formatISODate(article['publishedAt'])}")
					st.markdown(f"**Description:** {article['description']}")
					st.markdown(f"[Content:]({article['url']}) {article['content']}")
					st.markdown("\n---\n")
		else:
			st.error(data.get("message", "Unknown error"))
	except Exception as e:
		st.error(str(e))

def latestNews():
	st.title("Latest News")

	if not API_Exists():
		showInstructions()
		return

	required = st.selectbox("Required", [None] + list(REQUIRED.keys()))
	API = (st.secrets['api_key']["NEWS_API_KEY"] or os.environ["NEWS_API_KEY"])
	if required == "Top Headlines":
		col1, col2, col3 = st.columns(3)
		with col1:
			country = st.selectbox("Country", [None] + list(COUNTRIES.keys()))
		with col2:
			category = st.selectbox("Category", [None] + list(CATEGORIES.keys()))
		if st.button("Get News"):
			if country == None or category == None:
				st.error("Please select all the options")
			else:
				showHeadlines(API, required, country, category)
	elif required == "Everything":
		col1, col2 = st.columns(2)
		with col1:
			query = st.text_input("Enter your topic")
		with col2:
			sortby = st.selectbox("Sort By", [None] + list(SORTBY.keys()))
		if st.button("Get News") and query != "" and sortby != None:
			query = query.replace(" ", "+")
			showNews(API, required, query, sortby)
		else:
			st.error("Please enter a topic and select a sort by option")
