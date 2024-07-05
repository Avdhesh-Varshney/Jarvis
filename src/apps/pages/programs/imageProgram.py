import streamlit as st

def imagePrograms():
  st.title('Image Generator Programs')
  choice = st.selectbox('Select a program to execute', [None, "Barcode Generator", "QR Code Generator"])

  st.markdown('---')
  if choice == "Barcode Generator":
    from src.apps.pages.programs.ImageGenerators.barcode_maker import gen_barcode
    gen_barcode()

  st.markdown('---')
  if choice == "QR Code Generator":
    from src.apps.pages.programs.ImageGenerators.qr_code_generator import qrCodeGenerator
    qrCodeGenerator()
    
imagePrograms()
