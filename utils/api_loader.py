import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path='configs/.env')
LlaMa_API = os.getenv("LLAMA_API_KEY")
SawaAI = Groq(api_key=LlaMa_API)
DEEPLX_API_URL = os.getenv("DEEPLX_API_URL")
VOICEVOX_URL = os.getenv("VOICEVOX_URL")
SPEAKER_ID = os.getenv("SPEAKER_ID")

# YouTube_API = os.getenv("YOUTUBE_API_KEY")
