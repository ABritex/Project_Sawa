import requests
import json
import sounddevice as sd
import numpy as np
import soundfile as sf
from googletrans import Translator
import time
import configparser
from transformers import pipeline
import warnings
import os
warnings.filterwarnings("ignore", category=FutureWarning)

class Speech:
    def __init__(self, config_path="config.ini"):
        self.wav_path = "output.wav"
        self.config = self.load_config("config.ini")
        self.translator = Translator()
        self.voicevox_url = "http://127.0.0.1:50021"
        self.speaker_id = 6  # ID for a young female voice in VOICEVOX
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        
    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def translate_to_japanese(self, text):
        return self.translator.translate(text, dest='ja').text


    def analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)[0]
        return result['label'], result['score']

    def generate_voicevox_audio(self, text):
        sentiment, score = self.analyze_sentiment(text)
        print(f"Detected sentiment: {sentiment} with confidence: {score:.2f}")
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
        print("Audio generated...\n")
        self.play_audio(self.wav_path)

    def play_audio(self, file_path):
        data, fs = sf.read(file_path)
        sd.play(data, fs)
        sd.wait()  
        time.sleep(2)
        os.remove(file_path)  # Delete the WAV file after playing