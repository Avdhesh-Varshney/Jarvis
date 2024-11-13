import tensorflow as tf
import numpy as np
import streamlit as st
from PIL import Image
import gdown

@st.cache_resource
def load_model():
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['digitRecognizerModel']['MODEL_9']}", 'model_9.keras', quiet=False)
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['digitRecognizerModel']['MODEL']}", 'model.keras', quiet=False)
	model = tf.keras.models.load_model("model_9.keras")
	return model

def upload_digit_img():
	img = st.file_uploader("Upload here",type=["jpg","jpeg","png"])
	if img is not None: 
		try:
			st.image(img,width=200,caption="Uploaded Img")
			img_data = Image.open(img).convert("L") #grayscale image needed
			resized_img_data = img_data.resize((28, 28))
			input_arr = np.expand_dims(np.asarray(resized_img_data), (0, -1))

			return input_arr
		except Exception as e:
			st.error(f"Error is : {e}")
			return None
	else:
		st.warning("Please upload an image")
		return None

def model_test(x):
	model = load_model()
	y_pred = np.argmax(model.predict(x))
	return y_pred

def digitRecognizerModel():
	st.write("Upload a photo of the handwritten digit")
	input = upload_digit_img()

	if input is not None:
		y_pred = model_test(input)
		user = st.session_state["user"].split(',')
		name = user[2] + " " + user[3]
		st.success(f'Hi {name},\nThe number is {y_pred}', icon="🎉")
