import streamlit as st
import requests

# Function to fetch recipes from the Spoonacular API
def fetchRecipes(query):
    if query:
        api_key = st.secrets["SPOONACULAR"]["api_key"]  # Retrieve API key from Streamlit secrets
        api_url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={api_key}"
        response = requests.get(api_url)
        return response.json()
    return None

# Main function to handle the recipe finding logic
def recipeFinder():
    # Streamlit UI
    # Custom CSS
    st.write(
    """
    <style>
        /* Style for the main title */
        .title{
            flex-direction: column;
            font-size: 75px;
            color: white;
            position: absolute;
            top: 30px;
            text-align: center;
            left: 125px;
            z-index: 10;
        }
        /* Center the input container and input field */
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 30vh;
            flex-direction: column;
            font-size: 80px;
        }
        /* Style for the input field */
        .stTextInput > div > input {
            text-align: center;
            font-size: 30px;
            width: 400px;
            padding: 10px;
            margin-bottom: 20px;
        }
        /* Style for the button */
        .stButton > button {
            font-size: 24px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    # Displays the title with the custom class
    st.markdown('<h1 class="title">Recipe Finder</h1>', unsafe_allow_html=True)

    # Centered input box with the button in a flex container
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    # Create a horizontal layout for the input field and button
    query = st.text_input("Ingredients or a dish name, you name it!", placeholder="Enter", key="recipe_query")

    # Add button to trigger recipe search
    if st.button("Find Recipes"):
        if query:
            recipes_data = fetchRecipes(query)
            if recipes_data and 'results' in recipes_data:
                recipes = recipes_data['results']
                st.markdown('<div class="recipe-container">', unsafe_allow_html=True)
                for recipe in recipes:
                    recipe_url = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']}"
                    st.markdown(
                        f"""
                        <a href="{recipe_url}">
                            <div class="recipe-item">
                                <img class="recipe-image" src="{recipe['image']}" />
                                <div class="recipe-title">{recipe["title"]}</div>
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No recipes found. Please try again with a different query.")
        else:
            st.warning("Please enter a query before clicking the button.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Adds custom CSS for styling the recipe list
    st.markdown(
        """
        <style>
        .recipe-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 25px;
        }
        .recipe-item {
            flex: 0 0 48%;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(14, 14, 14, 0.2);
            padding: 15px;
            border-radius: 15px;
            background: #212121;
            text-align: center;
            transition: transform 0.2s ease-in-out;
        }
        .recipe-item:hover {
            transform: scale(1.05);
        }
        .recipe-title {
            margin-top: 10px;
            font-size: 30px;
            color: White;
        }
        .recipe-image {
            width: 50%;
            border-radius: 5px;
        }
        a {
            text-decoration: none;
            color: inherit;
        }
        a:hover {
            text-decoration: none;
            color: inherit;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )