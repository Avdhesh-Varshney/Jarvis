import torch
import cv2
import time
from ultralytics import YOLO
import streamlit as st

@st.cache_resource
def load_model(model_name):
    model = YOLO(f'src/apps/pages/models/ObjectDetectionModels/ObjectDetection/{model_name}.pt')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)

    if device == "cuda":
        model.half()
    return model

def initialize_session_state():
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'camera_option' not in st.session_state:
        st.session_state.camera_option = 0

def camera_selection():
    with st.form("camera_form"):
        st.session_state.camera_option = 0 if st.selectbox("What are you using", 
                                                          ("Laptop camera", "External camera")) == "Laptop camera" else 1
        # Model selection: "yolov8s" or "yolo11s"
        model_name = st.selectbox("Which model would you like to use?", ("yolov8s", "yolo11s"))
        
        start_button = st.form_submit_button("Start")
        if start_button:
            st.session_state.running = True
        
        return model_name  # Return selected model name



def objectDetection():
    initialize_session_state()
    model_name = camera_selection()
    model = load_model(model_name)
    
    # Camera selection form
  
    
    # Stop button (outside the form)
    if st.button("Stop", disabled=not st.session_state.running):
        st.session_state.running = False
        
    # Main detection loop
    if st.session_state.running:
        stframe = st.empty()
        cap = cv2.VideoCapture(st.session_state.camera_option)
        
        if not cap.isOpened():
            st.error("Failed to open camera")
            st.session_state.running = False
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        frame_count = 0
        frame_skip = 2
        target_fps = 30
        
        try:
            while st.session_state.running:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to grab frame")
                    break

                if frame_count % frame_skip == 0:
                    start_frame_time = time.time()
                    results = model(frame, conf=0.4)
                    annotated_frame = results[0].plot()
                    end_frame_time = time.time()

                    frame_time = end_frame_time - start_frame_time
                    fps = 1 / frame_time if frame_time > 0 else 0

                    if fps < target_fps:
                        frame_skip = min(frame_skip + 1, 10)
                    elif fps > target_fps + 5:
                        frame_skip = max(frame_skip - 1, 1)

                    # Display the frame
                    stframe.image(annotated_frame, channels="BGR", caption=f'FPS: {fps:.2f}')

                frame_count += 1

        finally:
            cap.release()
            stframe.empty()
    
    if not st.session_state.running:
        st.write("Object detection is stopped. Click 'Start' to begin.")

if __name__ == "__main__":
    st.title("Real-time Object Detection")
    objectDetection()