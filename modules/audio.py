import whisper
import os
import wave
import pyaudio
import keyboard
import warnings
import asyncio

warnings.filterwarnings("ignore", category=UserWarning, module="whisper")

model = whisper.load_model("base")

async def record_audio(output_path="sounds/input.wav", transcription_callback=None):
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
    if transcription_callback: 
        transcribed_text = await asyncio.to_thread(transcribe_audio, WAVE_OUTPUT_FILENAME)
        await transcription_callback(transcribed_text)  


def transcribe_audio(audio_file):
    if not os.path.exists(audio_file):
        print(f"Error: {audio_file} does not exist.")
        return ""
    try:
        result = model.transcribe(audio_file)
        transcribed_text = result['text']
        print(f"You (voice input): {transcribed_text}")
        return transcribed_text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
