import streamlit as st
from utils.predict import predict_message

st.title("Spam Detection System")
st.write("Enter a message to classify it as Spam or Not Spam.")

# Input field
user_input = st.text_area("Message")

if st.button("Classify"):
    if user_input.strip():
        prediction, confidence = predict_message(user_input)
        st.subheader(f"Prediction: {prediction}")
        st.write(f"Confidence: {confidence:.2%}")
    else:
        st.error("Please enter a valid message!")
