import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline

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

def camera_selection():
    form_key = "Text_input_form"  # Use a unique key for the form
    with st.form(form_key):
        st.session_state.input_text = st.text_input("Enter a prompt to generate Image:")
        
        start_button = st.form_submit_button("Generate Image")
        if start_button:
            st.session_state.running = True
        
        return st.session_state.input_text  # Return entered text

# Define the main function
def textToImageGenerator():
    prompt = camera_selection()
    
    if prompt:
        try:
            pipe = load_pipeline()

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
    else:
        st.warning("Please enter a prompt first.")

# Call the main function directly
textToImageGenerator()
