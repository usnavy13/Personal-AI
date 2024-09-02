#%%

import time
from picamera import PiCamera

def capture_image(file_path):
    camera = PiCamera()
    try:
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(file_path)
    finally:
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    capture_image('/home/pi/ai_assistant/test_files')

# %%
