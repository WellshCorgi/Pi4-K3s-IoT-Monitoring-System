import cv2
import time
import os
from datetime import datetime

rtsp_url = 'rtsp://1.247.226.190:8554/'
save_dir = './store_pic'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Set up video capture with FFmpeg backend and TCP transport
cap = cv2.VideoCapture(f"{rtsp_url}", cv2.CAP_FFMPEG)

# Retry until the stream is opened
while not cap.isOpened():
    print("Attempting to connect to RTSP stream...")
    time.sleep(5)
    cap = cv2.VideoCapture(f"{rtsp_url}", cv2.CAP_FFMPEG)

print("Connected to RTSP stream.")

ret, frame = cap.read()
if not ret:
    print("Error: Unable to read frame from RTSP stream.")
else:
    # Get current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"capture_{timestamp}.jpg")

    # Save the frame
    success = cv2.imwrite(filename, frame)
    if success:
        print(f"[Success] Saved {filename}")
    else:
        print(f"Error: Unable to save {filename}")

cap.release()
