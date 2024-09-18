import requests
import json
import sounddevice as sd
import numpy as np
import soundfile as sf
from googletrans import Translator
import time
import configparser

class Speech:
    def __init__(self, config_path="config.ini"):
        self.wav_path = "output.wav"
        self.config = self.load_config("config.ini")
        self.eleven_labs_api_key = self.config["elevenlabs"]["api_key"]
        self.eleven_labs_voice_id = self.config["elevenlabs"]["voice_id"]
        self.translator = Translator()
        self.voicevox_url = "http://127.0.0.1:50021"
        self.speaker_id = 6  # ID for a young female voice in VOICEVOX
        
    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def translate_to_japanese(self, text):
        return self.translator.translate(text, dest='ja').text
         # Return original text if translation fails

    def wait_for_voicevox(self, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(f"{self.voicevox_url}/version")
            if response.status_code == 200:
                # print("VOICEVOX is ready!")
                return True
            time.sleep(1)
        print("Timed out waiting for VOICEVOX to start")
        return False

    def generate_audio_with_eleven_labs(self, text):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.eleven_labs_voice_id}"
        headers = {
            "xi-api-key": self.eleven_labs_api_key,
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        })
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

        # Save audio file
        with open(self.wav_path, "wb") as f:
            f.write(response.content)
        self.play_audio(self.wav_path)

    def generate_voicevox_audio(self, text):
        if not self.wait_for_voicevox():
            print("VOICEVOX not available.")
            return
        japanese_text = self.translate_to_japanese(text)
            
        # Generate audio query
        query_payload = {"text": japanese_text, "speaker": self.speaker_id}
        query_response = requests.post(f"{self.voicevox_url}/audio_query", params=query_payload)
        query_response.raise_for_status()
        query_data = query_response.json()

        # Synthesize voice
        synthesis_payload = {"speaker": self.speaker_id}
        synthesis_response = requests.post(
            f"{self.voicevox_url}/synthesis",
            headers={"Content-Type": "application/json"},
            params=synthesis_payload,
            data=json.dumps(query_data)
        )
        synthesis_response.raise_for_status()

        # Save and play audio
        with open(self.wav_path, "wb") as f:
            f.write(synthesis_response.content)
        print("Audio....\n")
            
        self.play_audio(self.wav_path)


    def play_audio(self, file_path):
        data, fs = sf.read(file_path)
        sd.play(data, fs)
        sd.wait()  # Wait for playback to complete
        time.sleep(1)  
  