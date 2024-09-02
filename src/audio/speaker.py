#%%
import sounddevice as sd
import soundfile as sf
import numpy as np

def play_sound(file_path, volume=1.0, device=None):
    # Read the audio file
    data, fs = sf.read(file_path, dtype='float32')
    
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
    # List of devices to try (excluding device 1 which is input-only)
    devices_to_try = [0, 2, 3, 4, 5, 6, 7, 8]
    volumes_to_try = [1.0, 5.0, 10.0]

    for device in devices_to_try:
        for volume in volumes_to_try:
            print(f"\nTrying device: {device}, volume: {volume}")
            play_sound("/home/pi/ai_assistant/src/audio/temp_audio.wav", volume=volume, device=device)
            input("Press Enter to continue to the next test...")


# %%
 