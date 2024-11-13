import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import speech_recognition as sr

# Function to generate image
@st.cache_resource
def load_pipeline():
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the pipeline without float16 if using CPU
    if device == "cpu":
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)
        
    pipe.to(device)
    return pipe

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for speech...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        
        try:
            st.info("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
        return None

# Define the main function
def speech_textToImageGenerator():
    
    # Button to use speech recognition outside the form
    if st.button("Use Speech Recognition"):
        recognized_text = recognize_speech()
        if recognized_text:
            st.session_state.input_text = recognized_text

    # Text input form
    with st.form("Text_input_form"):
        prompt = st.text_input("Enter a prompt to generate Image:", st.session_state.get("input_text", ""))
        submit_button = st.form_submit_button("Generate Image")

    # Generate image if prompt is available
    if prompt and submit_button:
        try:
            pipe = load_pipeline()
            
            # Generate the image
            if torch.cuda.is_available():
                with torch.autocast("cuda"):
                    output = pipe(prompt + " 4k, High Resolution", guidance_scale=8.5)
            else:
                output = pipe(prompt + " 4k, High Resolution", guidance_scale=8.5)

            image = output.images[0]
            st.image(image, caption="Generated Image", use_column_width=True)

            # Optionally, save the image
            image.save('src/apps/pages/programs/ImageGenerators/generated_image.png')
            st.success("Image generated successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    elif submit_button:
        st.warning("Please enter a prompt first.")

