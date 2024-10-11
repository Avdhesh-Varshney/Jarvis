import streamlit as st
import requests
import base64

def getImage(height, width, isGrayscale, isWebpFormat, blur):
    fileFormat = "webp" if isWebpFormat else "jpg"
    params = []
    if isGrayscale:
        params.append('grayscale')
    if blur:
        params.append(f'blur={blur}')
    URL = f'https://picsum.photos/{width}/{height}.{fileFormat}' + '?' + '&'.join(params)

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            encoded_image = base64.b64encode(response.content).decode()
            st.session_state['encoded_image'] = encoded_image
            st.session_state['file_format'] = fileFormat
            st.session_state['real_image'] = response.content

            st.markdown(f'<img src="data:image/{fileFormat};base64,{encoded_image}" alt="Image" style="border-radius:8px; border:1px #bababa solid" /> </br>', unsafe_allow_html=True)

            st.download_button(
                label="Download Image",
                data=response.content,
                file_name=f'random_image.{fileFormat}',
                mime=f'image/{fileFormat}'
            )
        else:
            st.error('Could not get image. Please try again later.')

    except Exception as e:
        st.error(str(e))


def randomImagesGenerator():

    st.title('Random Image')

    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input('Select image height', 0, 700, 300)
        isGrayscale = st.checkbox('Grayscale')

    with col2:
        width = st.number_input('Select image width', 0, 800, 400)
        isWebpFormat = st.checkbox('JPG ➡️ Webp')

    blur = st.slider('Blur', 0, 10, 0)

    if st.button('Find'):
        getImage(height, width, isGrayscale, isWebpFormat, blur)

    else:
        if 'encoded_image' in st.session_state:
            fileFormat = st.session_state['file_format']
            st.markdown(
                f'<img src="data:image/{fileFormat};base64,{st.session_state["encoded_image"]}" alt="Image" style="border-radius:8px; border:1px #bababa solid" /> </br>',
                unsafe_allow_html=True
            )
            st.download_button(
                label="Download Image",
                data=st.session_state['real_image'],
                file_name=f'random_image.{fileFormat}',
                mime=f'image/{fileFormat}'
            )