import os
import requests
import json
import soundfile as sf
import sounddevice as sd
import asyncio
from transformers import pipeline  
import time
import warnings
from utils.api_loader import VOICEVOX_URL, SPEAKER_ID  # Import from your API loader

warnings.filterwarnings("ignore", category=FutureWarning)

class TTS:
    def __init__(self):
        self.wav_path = "sounds/output.wav"
        
        self.voicevox_url = VOICEVOX_URL
        self.speaker_id = SPEAKER_ID
        
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)[0]
        return result['label'], result['score']

    def generate_voicevox_audio(self, text):
        sentiment, score = self.analyze_sentiment(text)
        print(f"Detected sentiment: {sentiment} with confidence: {score:.2f}")
        query_payload = {"text": text, "speaker": self.speaker_id}
        query_response = requests.post(f"{self.voicevox_url}/audio_query", params=query_payload)
        query_response.raise_for_status()
        query_data = query_response.json()
        synthesis_payload = {"speaker": self.speaker_id}
        synthesis_response = requests.post(
            f"{self.voicevox_url}/synthesis",
            headers={"Content-Type": "application/json"},
            params=synthesis_payload,
            data=json.dumps(query_data)
        )
        synthesis_response.raise_for_status()
        with open(self.wav_path, "wb") as f:
            f.write(synthesis_response.content)
        print("Audio generated...\n")

    async def play_audio(self, file_path):
        data, fs = sf.read(file_path)
        sd.play(data, fs)
        await asyncio.sleep(len(data) / fs)
        sd.wait()
        time.sleep(3)
        # os.remove(file_path)  deletes the audio file
