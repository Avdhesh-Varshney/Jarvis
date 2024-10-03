import torch
import cv2
import time
from ultralytics import YOLO
import threading

# Load a smaller model for better speed
model = YOLO('yolov8n.pt')  # Change the model name according to your desired need. You can also use Yolo-v11 with the same code.
device = 'cuda' if torch.cuda.is_available() else 'cpu'  # use GPU for better performance
print(f"Using: - {device}")
model.to(device)

# If you are using GPU, then uncomment the below line.
# model.half()

# Capture the video stream from the webcam
cap = cv2.VideoCapture(0)

# Set the frame width and height (e.g., 640x480 for a smaller resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0
fps = 0  # Initialize FPS
start_time = time.time()  # Start time for FPS calculation
frame_skip = 2  # Start with an initial frame skip value
target_fps = 30  # Desired FPS

def object_detection():
    global frame_count, fps, frame_skip

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames dynamically to adjust processing speed
        if frame_count % frame_skip == 0:
            # Time before processing the frame
            start_frame_time = time.time()

            # Run object detection
            results = model(frame, conf=0.4, show=True)

            # Time after processing the frame
            end_frame_time = time.time()

            # Calculate FPS
            frame_time = end_frame_time - start_frame_time
            fps = 1 / frame_time  # FPS = 1 / Time per frame

            # Adjust frame skipping based on FPS
            if fps < target_fps:  # If FPS drops below target, skip more frames
                frame_skip = min(frame_skip + 1, 10)  # Cap frame skipping to avoid skipping too many
            elif fps > target_fps + 5:  # If FPS exceeds the target by a margin, reduce frame skipping
                frame_skip = max(frame_skip - 1, 1)  # Ensure frame_skip doesn't drop below 1

        frame_count += 1

# Start the frame processing in a separate thread
thread = threading.Thread(target=object_detection)
thread.start()

while True:
    # Capture frames separately while processing happens in the background
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
