import streamlit as st

def healthCareModels():
  st.title('Health Care Models')
  choice = st.selectbox('Choose any model', [None, 'Diabetes Test'])

  if choice == 'Diabetes Test':
    from src.apps.pages.models.HealthCareModels.DiabetesModel.diabetes import diabetes_test
    diabetes_test()

healthCareModels()
