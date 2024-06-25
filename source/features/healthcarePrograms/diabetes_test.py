import tensorflow as tf
import streamlit as st
def diabetesTestForm():
    details = []
    with st.form("dbtest"):
        col1,col2 = st.columns(2)
        details.append(col1.number_input("Pregnancies",min_value=0,step=1))
        details.append(col2.number_input("Glucose"))
        details.append(st.number_input("Blood pressure in mm Hg"))
        details.append(st.number_input("Triceps Skin Thickness in mm"))
        details.append(st.number_input("Insulin in mu U/ml"))
        details.append(st.number_input("BMI"))
        details.append(st.number_input("Age",min_value=1,step=1))
        btn = st.form_submit_button("Submit")
        return details,btn

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('source\models\dlModels\diabetes_test_model.keras')
    return model


def do_diabetes_test(input):
    model = load_model()
    res = model.predict(input)
    if res*100 > 50 :
        return 1
    else :
       return 0

