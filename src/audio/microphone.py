#%%
import pyaudio
import wave
import numpy as np
from collections import deque
from openai import OpenAI
import logging
from dotenv import load_dotenv
import os
import time
import threading
from queue import Queue
import io

# Load environment variables
load_dotenv()

# Add this line to get the listening time from the environment variable


# Initialize OpenAI client
client = OpenAI()

logger = logging.getLogger(__name__)

# Audio parameters
CHUNK = 4096  # Increase buffer size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Match the default sample rate of the device
THRESHOLD = int(os.getenv("THRESHOLD", "1000"))
SILENCE_LIMIT = float(os.getenv("SILENCE_LIMIT", "2"))
PRE_RECORD_SECONDS = float(os.getenv("PRE_RECORD_SECONDS", "0.5"))
DEVICE_INDEX = 2  # UM02: USB Audio device
LISTENING_TIME = int(os.getenv("LISTENING_TIME", "5"))

def is_silent(data):
    """Returns 'True' if below the 'silent' threshold"""
    return max(data) < THRESHOLD

def transcribe_audio(audio_data):
    # Create an in-memory binary stream
    audio_buffer = io.BytesIO()
    
    # Write audio data to the buffer
    with wave.open(audio_buffer, 'wb') as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wav_file.setframerate(RATE)
        wav_file.writeframes(b''.join(audio_data))
    
    # Reset buffer position to the beginning
    audio_buffer.seek(0)

    start_time = time.time()  # Start timing
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=("audio.wav", audio_buffer)
    )
    
    end_time = time.time()  # End timing
    
    transcription_time = end_time - start_time
    logger.info(f"Transcription took {transcription_time} seconds")
    
    return transcription.text

def transcribe_audio_in_background(audio_data, transcription_queue):
    transcription = transcribe_audio(audio_data)
    transcription_queue.put(transcription)

def cleanup(stream, p):
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()

def listen():
    p = None
    stream = None
    try:
        p = pyaudio.PyAudio()
        
        # Get the device info
        device_info = p.get_device_info_by_index(DEVICE_INDEX)
        channels = min(CHANNELS, device_info['maxInputChannels'])
        rate = min(RATE, int(device_info['defaultSampleRate']))
        
        stream = p.open(format=FORMAT, 
                        channels=channels, 
                        rate=rate, 
                        input=True, 
                        frames_per_buffer=CHUNK, 
                        input_device_index=DEVICE_INDEX)
        
        print("* Listening...")

        audio = []
        silent_chunks = 0
        recording = False
        listening_start_time = time.time()
        return_none = False

        # Calculate the number of chunks needed for pre-recording
        pre_record_chunks = int(PRE_RECORD_SECONDS * rate / CHUNK)

        # Create a deque to store the pre-record buffer
        pre_record_buffer = deque(maxlen=pre_record_chunks)

        while True:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    print("Input overflowed, ignoring")
                    continue
                else:
                    raise

            audio_data = np.frombuffer(data, dtype=np.int16)

            if not is_silent(audio_data):
                listening_start_time = time.time()  # Reset the timer when sound is detected
                if not recording:
                    print("* Recording...")
                    recording = True
                    # Add the pre-record buffer to the audio
                    audio.extend(list(pre_record_buffer))
                silent_chunks = 0
                audio.append(data)
            elif recording:
                silent_chunks += 1
                audio.append(data)

                if silent_chunks > SILENCE_LIMIT * rate / CHUNK:
                    print("* Finished recording")
                    break
            else:
                # If not recording, add the chunk to the pre-record buffer
                pre_record_buffer.append(data)
                
                # Check if LISTENING_TIME seconds have passed without detecting sound
                if time.time() - listening_start_time > LISTENING_TIME:
                    print(f"* No sound detected for {LISTENING_TIME} seconds.")
                    return_none = True
                    break

        if return_none:
            return None

        if recording:
            # Transcribe the audio in the background
            transcription_queue = Queue()
            transcription_thread = threading.Thread(target=transcribe_audio_in_background, args=(audio, transcription_queue))
            transcription_thread.start()

            # Get the transcription result
            transcription = transcription_queue.get()
            print(f"Transcription: {transcription}")

            # Return the transcription
            return transcription
        
    except (OSError, ValueError) as e:
        print(f"Error opening stream: {e}")
        print(f"Device info: {device_info}")
        return None
    finally:
        cleanup(stream, p)

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        max_input_channels = device_info.get('maxInputChannels')
        if max_input_channels > 0:
            print(f"Input Device {i}: {device_name}")
    
    p.terminate()

if __name__ == "__main__":
    list_audio_devices()  # Add this line to print the devices when the script is run
    while True:
        result = listen()
        if result:
            print(f"Final result: {result}")
        else:
            print("No input detected. Listening again...")
# %%
