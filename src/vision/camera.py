import cv2
import base64
import numpy as np

def capture_image_base64():
    print("Capturing image")
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set camera properties
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 5)
    cap.set(cv2.CAP_PROP_CONTRAST, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Capture an image
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    if ret:
        # Encode the image to base64
        _, buffer = cv2.imencode('.jpg', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        print("Image captured and converted to base64 successfully!")
        return base64_image
    else:
        print("Failed to capture image")
        return None

# Example usage:
#base64_image = capture_image_base64()


