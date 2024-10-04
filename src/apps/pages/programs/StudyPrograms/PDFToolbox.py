import streamlit as st
import PyPDF2

def readPDF():
  st.markdown("#### PDF Reader App")
  file = st.file_uploader("Upload a PDF file", type=["pdf"])
  if not file:
    st.stop()
  reader = PyPDF2.PdfReader(file)
  numPage = st.number_input("From which page I have to start reading?", format="%d", min_value=1, max_value=len(reader.pages))
  page = reader.pages[numPage-1]
  text = page.extract_text()
  if text:
    st.write(text)
  else:
    st.warning("No text found in this page", icon="⚠️")

# TODO: Implement mergePDF, splitPDF, rotatePDF, encryptPDF, decryptPDF functions
def PDFToolbox():
  st.title("PDF Reader & Editor App")
  choice = st.selectbox("Choose an operation", [None, "Read PDF", "Merge PDF", "Split PDF", "Rotate PDF", "Encrypt PDF", "Decrypt PDF"])
  if choice == "Read PDF":
    readPDF()
  elif choice == "Merge PDF":
    st.info("Coming soon!", icon="🚧")
  elif choice == "Split PDF":
    st.info("Coming soon!", icon="🚧")
  elif choice == "Rotate PDF":
    st.info("Coming soon!", icon="🚧")
  elif choice == "Encrypt PDF":
    st.info("Coming soon!", icon="🚧")
  elif choice == "Decrypt PDF":
    st.info("Coming soon!", icon="🚧")
  else:
    st.warning("Invalid choice!", icon="⚠️")
