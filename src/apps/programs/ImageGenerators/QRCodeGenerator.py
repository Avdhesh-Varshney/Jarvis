import streamlit as st
import qrcode
import io

def QRCodeGenerator():
    st.title("QR Code Generator")
    
    input_data = st.text_input("Enter data for the QR Code (text, link, number, etc.):")
    
    if st.button("Generate QR Code"):
        if input_data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(input_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(byte_im, caption="Generated QR Code", use_column_width=True)

            st.download_button(
                label="Download QR Code",
                data=byte_im,
                file_name="qr_code.png",
                mime="image/png"
            )
        else:
            st.error("Please enter some data to generate the QR code.")

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
        """,
            unsafe_allow_html=True,
        )
