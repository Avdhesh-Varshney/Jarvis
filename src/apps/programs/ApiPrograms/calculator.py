import streamlit as st
import requests

# Wolfram Alpha API Base URL
WOLFRAM_URL = "http://api.wolframalpha.com/v2/query"

# Function to perform Wolfram Alpha query
def calculate_expression(query, wolfram_api_key):
    # API request parameters
    params = {
        'input': query,
        'format': 'image,plaintext',
        'output': 'JSON',
        'appid': wolfram_api_key
    }
    
    # Making API request
    response = requests.get(WOLFRAM_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'queryresult' in data and data['queryresult']['success']:
            pods = data['queryresult']['pods']
            return pods
        else:
            st.error("No results found for the given input!", icon='🚨')
            return None
    else:
        st.error("Error fetching data from Wolfram Alpha", icon='🚨')
        return None

# Function to display plots 
def display_plots(pods):
    found_plot = False  
    for pod in pods:
        if 'img' in pod['subpods'][0]:  
            image_url = pod['subpods'][0]['img']['src']
            st.image(image_url, caption=pod['title'], use_column_width=True)
            found_plot = True
    
    if not found_plot:
        st.warning("No plots found for the given input!", icon='⚠️')

# Displaying the results of the query
def display_results(pods):
    if pods:
        for pod in pods:
            st.subheader(pod['title'])
            # Display text results
            if 'plaintext' in pod['subpods'][0] and pod['subpods'][0]['plaintext']:
                st.text(pod['subpods'][0]['plaintext'])
            # Display plots (only from display_plots)
        display_plots(pods)
    else:
        st.error("No results found for the given input!", icon='🚨')

# Main function
def calculator():
    st.title("Jarvis Calculator")

    # Get Wolfram API Key from secrets
    WOLFRAM_API_KEY = st.secrets["WOLFRAM_API_KEY"]

    # User Input for Mathematical Query
    query = st.text_input("Enter a mathematical expression to calculate (e.g., '5 + 5', 'integrate x^2 dx', 'solve x^2 + 5x = 0')")

    if st.button("Calculate"):
        if query:
            st.info(f"Query: {query}", icon="ℹ️")
            
            # Perform the Wolfram Alpha query
            result_pods = calculate_expression(query, WOLFRAM_API_KEY)
            
            # Display the results
            display_results(result_pods)
        else:
            st.error("Please enter a valid query!", icon="🚨") 