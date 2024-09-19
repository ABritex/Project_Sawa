import keyboard 
import pyaudio
import wave
import os
from modules.globals import process_input
import whisper 
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
from colorama import Fore, Back, Style

red, green, blue, yellow, fr = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RESET 

model = whisper.load_model("base")
def record_audio(output_path="sounds/input.wav"):
    CHUNK = 1024  
    FORMAT = pyaudio.paInt16 
    CHANNELS = 1  
    RATE = 44100  
    WAVE_OUTPUT_FILENAME = output_path
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    print("Recording...")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")
    transcribe_audio(WAVE_OUTPUT_FILENAME)

def transcribe_audio(audio_file):
    # print(f"Transcribing audio from {audio_file}...")
    if not os.path.exists(audio_file):
        print(f"Error: {audio_file} does not exist.")
        return ""
    try:
        result = model.transcribe(audio_file)
        transcribed_text = result['text']
        print(f"{green}You (voice input){fr}: {green}{transcribed_text}{fr}")
        process_input(transcribed_text)
    except Exception as e:
        print(f"Error during transcription: {e}")

def main():
    print(f"{blue}Choose an option{fr}:")
    print(f"{blue}1. Type your input{fr}")
    print(f"{blue}2. Voice input{fr}")

    choice = input(f"{blue}Enter 1 or 2{fr}: ").strip()

    if choice == "1":
        while True:
            user_input = input(f"\n{green}You{fr}: ")
            process_input(user_input)

    elif choice == "2":
        print("\nHold Right [Shift] to record audio")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                record_audio()  
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
