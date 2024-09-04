#%%
import sounddevice as sd
import soundfile as sf
import openai
from pathlib import Path

def speak(text, volume=5.0, device=2):
    client = openai.Client()
    speech_file_path = "/home/pi/ai_assistant/temp_audio.wav"

    # Generate speech from text
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(speech_file_path)

    # Read the audio file
    data, fs = sf.read(speech_file_path, dtype='float32')
    
    # Adjust the volume
    data = data * volume

    # Play the sound
    try:
        sd.play(data, fs, device=device)
        sd.wait()  # Wait until the audio is finished playing
    except sd.PortAudioError as e:
        print(f"Error playing audio: {e}")

# Example usage
if __name__ == "__main__":
    speak("The quick brown fox jumped over the lazy dog.")


# %%
