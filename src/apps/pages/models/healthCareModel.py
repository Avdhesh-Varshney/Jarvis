import streamlit as st

def healthCareModels():
  st.title('Health Care Models')
  choice = st.selectbox('Choose any model', [None, 'Diabetes Test','Brain Tumor Test'])

  st.markdown('---')

  if choice == 'Diabetes Test':
    from src.apps.pages.models.HealthCareModels.DiabetesModel.diabetes import diabetes_test
    diabetes_test()
    
  elif choice == 'Brain Tumor Test':
    from src.apps.pages.models.HealthCareModels.BrainTumorModel.brainTumor import brain_tumor_test
    brain_tumor_test()
    
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis) if you like it!", icon='⭐')

healthCareModels()
