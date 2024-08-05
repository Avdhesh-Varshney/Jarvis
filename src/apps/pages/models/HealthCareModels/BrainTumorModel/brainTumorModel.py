import tensorflow as tf
import streamlit as st
import numpy as np
from src.utils.english import Speak
from PIL import Image

@st.cache_resource
def load_model():
  model = tf.keras.models.load_model("src/apps/pages/models/HealthCareModels/BrainTumorModel/brain_tumor_test.keras")
  return model

def get_mri():
  img = st.file_uploader("Upload here",type=["jpg","jpeg"])
  codn = False
  data = []
  if img is not None:
    st.image(img,width=420,caption="Uploaded Img")
    data = Image.open(img).convert("RGB" )
    data = data.resize((64,64))
    data = np.asarray(data)
    data = np.expand_dims(data,axis=0)
    codn = True

  return codn,data

def do_test(img):
  model = load_model()
  res = np.argmax(model.predict(img))
  return res

def brainTumorModel():
  st.write("Please Upload MRI Scan of Brain")
  codn,img = get_mri()
  res = None

  if codn!=False:
    res = do_test(img)

  if res!=None:     
    if res == 0:
      st.error(f'Hi {st.session_state.name},\nYou are diagnosed with Glioma.\nPlease consult a doctor.')
      Speak(f'Hi {st.session_state.name},You are diagnosed with Glioma. Please consult a doctor.')
    elif res == 1:
      st.error(f'Hi {st.session_state.name},\nYou are diagnosed with Meningioma.\nPlease consult a doctor.')
      Speak(f'Hi {st.session_state.name},You are diagnosed with Meningioma. Please consult a doctor.')
    elif res == 2:
      st.success(f'Congrats {st.session_state.name}, You are not diagnosed with brain tumor.')
      Speak(f'Congrats {st.session_state.name}, You are not diagnosed with brain tumor.')
    elif res == 3:
      st.error(f'Hi {st.session_state.name},\nYou are diagnosed with Pituitary tumor. Please consult a doctor.')
      Speak(f'Hi {st.session_state.name},You are diagnosed with Pituitary tumor. Please consult a doctor.')
    codn = False
