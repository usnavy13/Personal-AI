#%%
import base64
import time
import logging

logger = logging.getLogger(__name__)

def image_to_base64(image_path: str) -> str:
    """
    Convert an image to a base64 string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded string of the image.
    """
    logger.info(f"Starting conversion of image: {image_path}")
    start_time = time.time()  # Start timing
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        end_time = time.time()  # End timing
        processing_time = end_time - start_time
        logger.info(f"Successfully converted image: {image_path} in {processing_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error converting image: {image_path}, Error: {e}")
        raise
    return encoded_string

# Example usage:
#base64_string = image_to_base64("/home/pi/ai_assistant/z3rNHS9Y6PV6vbhH8w83Yn-1000-80.jpg.webp")

# Example usage:

# %%
