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
            flex-direction: column; /* Align the label and input field in a column */
            font-size: 75px; /* Adjust title size */
            color: white; /* Title color */
            position: absolute; /* Positioning the title */
            top: 30px; /* Distance from the top */
            text-align: center; /* Center vertically */
            left: 125px; /* Distance from the left */
            z-index: 10; /* Ensures the title is on top */
        }
        /* Center the input container and input field */
        .input-container {
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            height: 30vh; /* Adjust height to align vertically */
            flex-direction: column; /* Align the label and input field in a column */
            font-size: 80px; /* Adjust input text size */
        }
        /* Style for the input field */
        .stTextInput > div > input {
            text-align: center; /* Center the text in the input field */
            font-size: 30px; /* Adjust input text size */
            width: 400px; /* Adjust input width */
            padding: 10px; /* Padding inside input */
            margin-bottom: 20px; /* Add space below the input field */
        }
        /* Style for the input label */
        .stTextInput > label {
            text-align: center; /* Center the label text */
            font-size: 30px; /* Adjust label text size */
            display: block;
        }
        /* Style for the button */
        .stButton > button {
            font-size: 24px; /* Button text size */
            padding: 10px 20px; /* Padding for button */
        }
        .stButton > button:hover {
            transform: scale(1.05); /* Optional hover effect */
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
        # Ensure the query is not empty before fetching recipes
        if query:
            # Fetch recipes
            recipes_data = fetchRecipes(query)
            
            if recipes_data and 'results' in recipes_data:
                # Extract the results list from the response
                recipes = recipes_data['results']
                
                # Creates a flex container for the recipes
                st.markdown('<div class="recipe-container">', unsafe_allow_html=True)
                
                # Displays each recipe with the updated styles
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
                st.warning("No recipes found. Please try again with a different query.")  # Notify the user
        else:
            st.warning("Please enter a query before clicking the button.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Adds custom CSS for styling the recipe list
    st.markdown(
        """
        <style>
        .recipe-container {
            display: flex;
            flex-wrap: wrap; /* Allows items to wrap onto multiple lines */
            justify-content: space-between; /* Adjusts spacing between items */
            margin-bottom: 25px; /* Space between rows */
        }
        .recipe-item {
            flex: 0 0 48%; /* Adjusts width of each item */
            margin-bottom: 10px; /* Space between items */
            box-shadow: 0 2px 5px rgba(14, 14, 14, 0.2); /* Optional: adds shadow */
            padding: 15px; /* Padding for inner content */
            border-radius: 15px; /* Rounds the corners */
            background: #212121; /* Background color for the item */
            text-align: center; /* Centering the text */
            transition: transform 0.2s ease-in-out;
        }
        .recipe-item:hover {
            transform: scale(1.05); /* Optional hover effect */
        }
        .recipe-title {
            margin-top: 10px;
            font-size: 30px; /* Increase text size */
            color: White;
        }
        .recipe-image {
            width: 50%;
            border-radius: 5px; /* Rounded corners for the image */
        }
        a {
            text-decoration: none;
            color: inherit;
        }
        a:hover {
            text-decoration: none; /* Removes the underline on hover */
            color: inherit; /* Ensures no color change on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call the main function to run the app
recipeFinder()