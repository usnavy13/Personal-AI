#%%
import time
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

client = OpenAI()

def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    
    start_time = time.time()  # Start timing
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=audio_file
    )
    
    end_time = time.time()  # End timing
    
    transcription_time = end_time - start_time
    logger.info(f"Transcription took {transcription_time} seconds")
    
    return transcription.text

# Example usage:
#text = transcribe_audio("/home/pi/ai_assistant/test_files/Recording.m4a")
#print(text)
# %%
