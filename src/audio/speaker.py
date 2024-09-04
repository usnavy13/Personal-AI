#%%
import sounddevice as sd
import soundfile as sf
import openai
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

VOLUME = float(os.getenv("VOLUME", "5.0"))
VOICE = os.getenv("VOICE", "alloy")
DEVICE = int(os.getenv("DEVICE", "2"))
VOICE_MODEL = os.getenv("VOICE_MODEL", "tts-1")

def speak(text):
    if text == '':
        return None
    client = openai.Client()
    speech_file_path = "/home/pi/ai_assistant/temp_audio.wav"

    # Generate speech from text
    with client.audio.speech.with_streaming_response.create(
        model=VOICE_MODEL,
        voice=VOICE,
        input=text
    ) as response:
        response.stream_to_file(speech_file_path)

    # Read the audio file
    data, fs = sf.read(speech_file_path, dtype='float32')
    
    # Adjust the volume
    data = data * VOLUME

    # Play the sound
    try:
        sd.play(data, fs, device=DEVICE)
        sd.wait()  # Wait until the audio is finished playing
    except sd.PortAudioError as e:
        print(f"Error playing audio: {e}")

# Example usage
if __name__ == "__main__":
    speak("The quick brown fox jumped over the lazy dog.")


# %%
