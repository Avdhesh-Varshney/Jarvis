from barcode.writer import ImageWriter
from barcode import EAN13, EAN8, UPCA
import streamlit as st
import base64

# Set barcode type
BARCODE_TYPE = {"EAN-13": [13, EAN13], "EAN-8": [8, EAN8], "UPCA": [12, UPCA]}

def barCodeGenerator():
    box = st.container() # To keep everything inside one container
    with box:
        option = st.radio(
            "Select type of Barcode", ["EAN-13", "EAN-8", "UPCA"], horizontal=True
        )
        num = st.text_input(
            "Enter barcode number",
            value="",
            max_chars=BARCODE_TYPE[option][0],
            placeholder=f"Enter {BARCODE_TYPE[option][0]} digits long barcode number",
        )
        button_div = st.empty() # So that when Generate Barcode is pressed, it will be replaced by Reset button
    
    with button_div:
        if st.button("Generate barcode"): 
            generate(num, box, option)
            st.button("Reset barcode") # Resets everything


def generate(num, box, option):
    with box:
        if len(num) != BARCODE_TYPE[option][0] or not num.isnumeric():
            st.warning(
                f"Please enter a valid {option} barcode of {BARCODE_TYPE[option][0]} digits!!"
            )
        else:
            # Included ImageWriter to save the image in png format
            image_path = "assets/barcode"

            my_code = BARCODE_TYPE[option][1](num, writer=ImageWriter())
            my_code.save(image_path)

            with open(f"{image_path}.png", "rb") as file:
                image_data = file.read()

            encoded_image = base64.b64encode(image_data).decode()

            # For custom styling of image and button
            st.markdown(
                f"""
                <style>
                .button-container {{
                    display: flex;
                    justify-content: space-around;  /* Adjust as needed: space-between, space-around, etc. */
                }}
                .styled-button {{
                    background-color: #ff4b4b;  /* Default button background color */
                    color: white;  /* Default button text color */
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s, color 0.3s;  /* Transition effect for color change */
                }}
                .styled-button:hover {{
                    background-color: #ff3333;  /* Button background color on hover */
                    color: white;  /* Button text color on hover */
                }}
                </style>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/png;base64,{encoded_image}" alt="Your Image">
                    <br>
                    <a href="data:image/png;base64,{encoded_image}" download="barcode.png">
                        <button class="styled-button">Download Image</button>
                    </a>
                </div>
            """,
                unsafe_allow_html=True,
            )
