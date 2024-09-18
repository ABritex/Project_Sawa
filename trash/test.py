import requests
import configparser
import os
from pydub import AudioSegment
import simpleaudio as sa

class Speech:
    def init(self):
        self.config = self.load_config("config.ini")
        self.api_key = self.config["elevenlabs"]["api_key"]
        self.voice_id = self.config["elevenlabs"]["voice_id"]
        self.mp3_path = "output.mp3"
        self.wav_path = "output.wav"

    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def generate_audio(self, text):
        try:
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"

            headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key
            }

            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }

            response = requests.post(tts_url, headers=headers, json=data, stream=True)

            if response.ok:
                with open(self.mp3_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print("Audio generated successfully.")

                # Convert MP3 to WAV
                self.convert_mp3_to_wav(self.mp3_path, self.wav_path)

                # Play the audio file using simpleaudio
                self.play_audio(self.wav_path)

                # Optionally clean up the files
                os.remove(self.mp3_path)
                os.remove(self.wav_path)
            else:
                print(f"Error generating audio: {response.text}")
        except Exception as e:
            print(f"Error generating audio: {e}")

    def convert_mp3_to_wav(self, mp3_path, wav_path):
        try:
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(wav_path, format="wav")
            print("Converted MP3 to WAV successfully.")
        except Exception as e:
            print(f"Error converting MP3 to WAV: {e}")

    def play_audio(self, file_path):
        try:
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        except Exception as e:
            print(f"Error playing audio: {e}")

# Example usage
if name == "main":
    speech = Speech()
    speech.generate_audio("Hello, how are you today?")


