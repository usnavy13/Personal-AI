#%%
import sounddevice as sd
import soundfile as sf
import openai
import io
import os
from dotenv import load_dotenv
import numpy as np
from scipy import signal

load_dotenv()

VOLUME = float(os.getenv("VOLUME", "5.0"))
VOICE = os.getenv("VOICE", "alloy")
DEVICE = 1#int(os.getenv("DEVICE", "2"))
VOICE_MODEL = os.getenv("VOICE_MODEL", "tts-1")

def speak(text):
    if text == '':
        return None
    client = openai.Client()

    # Generate speech from text
    with client.audio.speech.with_streaming_response.create(
        model=VOICE_MODEL,
        voice=VOICE,
        input=text
    ) as response:
        # Read the audio data into memory
        audio_data = io.BytesIO(response.read())

    # Read the audio data from memory
    data, fs = sf.read(audio_data, dtype='float32')
    print(f"Original audio sample rate: {fs} Hz")

    # Get the default sample rate of the output device
    device_info = sd.query_devices(DEVICE, 'output')
    device_fs = int(device_info['default_samplerate'])
    print(f"Device sample rate: {device_fs} Hz")

    # Resample if necessary
    if fs != device_fs:
        print(f"Resampling from {fs} Hz to {device_fs} Hz")
        number_of_samples = round(len(data) * float(device_fs) / fs)
        data = signal.resample(data, number_of_samples)
        fs = device_fs

    # Adjust the volume
    data = data * VOLUME

    # Play the sound
    try:
        sd.play(data, fs, device=DEVICE)
        sd.wait()  # Wait until the audio is finished playing
    except sd.PortAudioError as e:
        print(f"Error playing audio: {e}")

def print_speaker_devices():
    devices = sd.query_devices()
    print("Available speaker devices:")
    for i, device in enumerate(devices):
        if device['max_output_channels'] > 0:
            print(f"{i}: {device['name']}")
            print(f"   Supported sample rates: {device['default_samplerate']} Hz")

# Example usage
if __name__ == "__main__":
    print_speaker_devices()
    speak("The quick brown fox jumped over the lazy dog.")


# %%
