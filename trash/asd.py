import sounddevice as sd

def list_devices():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")

list_devices()



# Example usage
if __name__ == "__main__":
    speech = Speech()
    
    # Step 1: Generate English audio using Eleven Labs
    speech.generate_audio_with_eleven_labs("Hello, how are you today?")
    
    # Step 2: Translate to Japanese and generate Japanese voice using VOICEVOX (optional)
    speech.generate_voicevox_audio("Hello, how are you today?")
