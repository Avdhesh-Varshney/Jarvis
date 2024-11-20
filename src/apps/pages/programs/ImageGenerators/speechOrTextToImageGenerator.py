from diffusers import StableDiffusionPipeline
from src.utils.english import Listen
import streamlit as st
import torch

@st.cache_resource
def load_pipeline():
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    if device == "cpu":
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)

    pipe.to(device)
    return pipe

def speechOrTextToImageGenerator():
    st.markdown("## Speech or Text to Image Generator")
    st.write("This program generates an image based on the input prompt. You can either enter a prompt manually or use speech recognition to enter the prompt.")

    choice = st.radio("Select input method:", ["Text", "Speech"])
    prompt = None

    if choice == "Text":
        prompt = st.text_input("Enter a prompt to generate Image:", st.session_state.get("input_text", ""))
    else:
        prompt = Listen()

    submit_button = st.button("Generate Image")
    if prompt and submit_button:
        try:
            pipe = load_pipeline()
            if torch.cuda.is_available():
                with torch.autocast("cuda"):
                    output = pipe(prompt + " 4k, High Resolution", guidance_scale=8.5)
            else:
                output = pipe(prompt + " 4k, High Resolution", guidance_scale=8.5)

            image = output.images[0]
            st.image(image, caption="Generated Image", use_column_width=True)
            image.save('generated_image.png')
            st.success("Image generated successfully!", icon="🎉")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}", icon="🚫")

    elif submit_button:
        st.warning("Please enter a prompt first.", icon="⚠️")
