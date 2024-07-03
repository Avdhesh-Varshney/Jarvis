import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# Set up the page title and layout
st.set_page_config(page_title="Dynamic QR Code Generator", layout="centered")
st.title("Dynamic QR Code Generator")

# Get user input
input_data = st.text_area("Enter the data for the QR Code (e.g., text, link, phone number, etc.)", "")

if input_data:
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Display the QR code
    st.image(img, caption="Generated QR Code", use_column_width=True)

    # Save the QR code image to a buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Download button for the QR code image
    st.download_button(
        label="Download QR Code",
        data=buffer,
        file_name="qr_code.png",
        mime="image/png",
    )
else:
    st.write("Please enter some data to generate a QR code.")

# Add some styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
