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

# Load environment variables
load_dotenv()
ACTIVATION_WORD = os.getenv("ACTIVATION_WORD")

# Initialize OpenAI client
client = OpenAI()

logger = logging.getLogger(__name__)

# Audio parameters
CHUNK = 4096  # Increase buffer size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Match the default sample rate of the device
THRESHOLD = 1000  # Adjust this value to set the volume threshold for speech detection
SILENCE_LIMIT = 2  # Number of seconds of silence before stopping the recording
PRE_RECORD_SECONDS = 0.5  # Number of seconds to save before speech is detected
DEVICE_INDEX = 1  # UM02: USB Audio device

def is_silent(data):
    """Returns 'True' if below the 'silent' threshold"""
    return max(data) < THRESHOLD

def transcribe_audio(audio_data):
    audio_file = wave.open("temp_audio.wav", 'wb')
    audio_file.setnchannels(CHANNELS)
    audio_file.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    audio_file.setframerate(RATE)
    audio_file.writeframes(b''.join(audio_data))
    audio_file.close()

    with open("temp_audio.wav", "rb") as audio_file:
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

def transcribe_audio_in_background(audio_data, transcription_queue):
    transcription = transcribe_audio(audio_data)
    transcription_queue.put(transcription)

def record_audio():
    p = pyaudio.PyAudio()
    
    # List all available audio devices
    print("\nAvailable audio devices:")
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {dev_info['name']}")
        print(f"  Max Input Channels: {dev_info['maxInputChannels']}")
        print(f"  Default Sample Rate: {dev_info['defaultSampleRate']}")
    
    # Get the device info
    device_info = p.get_device_info_by_index(DEVICE_INDEX)
    channels = device_info['maxInputChannels']
    rate = int(device_info['defaultSampleRate'])
    
    # Adjust parameters if necessary
    channels = min(CHANNELS, channels)
    rate = min(RATE, rate)
    
    print(f"\nUsing Device {DEVICE_INDEX}: {device_info['name']}")
    print(f"Channels: {channels}")
    print(f"Sample Rate: {rate}")
    
    try:
        stream = p.open(format=FORMAT, 
                        channels=channels, 
                        rate=rate, 
                        input=True, 
                        frames_per_buffer=CHUNK, 
                        input_device_index=DEVICE_INDEX)
        
        while True:
            print("* Listening...")

            audio = []
            silent_chunks = 0
            recording = False

            # Calculate the number of chunks needed for pre-recording
            pre_record_chunks = int(PRE_RECORD_SECONDS * rate / CHUNK)

            # Create a deque to store the pre-record buffer
            pre_record_buffer = deque(maxlen=pre_record_chunks)

            try:
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

                # Transcribe the audio in the background
                transcription_queue = Queue()
                transcription_thread = threading.Thread(target=transcribe_audio_in_background, args=(audio, transcription_queue))
                transcription_thread.start()

                # Continue recording while transcription is happening
                while transcription_thread.is_alive():
                    data = stream.read(CHUNK)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    if not is_silent(audio_data):
                        audio.append(data)

                # Get the transcription result
                transcription = transcription_queue.get()
                print(f"Transcription: {transcription}")

                # Check for "stop listening" phrase
                if "stop listening" in transcription.lower():
                    print("* Stop listening command detected")
                    return None

                # Return the transcription
                return transcription

            except KeyboardInterrupt:
                print("Stopping...")
                break

        stream.stop_stream()
        stream.close()
        p.terminate()

    except (OSError, ValueError) as e:
        print(f"Error opening stream: {e}")
        print(f"Device info: {device_info}")
        p.terminate()
        return None

if __name__ == "__main__":
    record_audio()

# %%
