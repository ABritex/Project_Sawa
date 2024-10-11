from modules.audio import record_audio
from modules.translate import translate_text
from modules.katakana import convert_to_katakana
from modules.romanize import romanji_translate
from modules.tts import TTS
from modules.youtube import fetch_and_handle_messages
from llm.SawaAI import handle_input
from llm.Sawa_State import SawaState
from llm.memory import Memory
from utils.chat_handler import ChatHandler
from colorama import Fore

red, green, blue, yellow, cyan, fr = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.RESET 

class GlobalState:
    def __init__(self):
        self.current_state = "idle"
        self.message_history = []
        self.user_inputs = {}
        self.llm_response = None
        self.sawa_state = SawaState()
        self.chat_handler = ChatHandler()  
        self.tts = TTS()
        self.memory = Memory() 

    async def handle_input_event(input_text):
        await global_state.process_input(input_text)

    async def process_input(self, input_text, source=None):
        if source != 'youtube_chat':
            response = handle_input(input_text)  
            self.llm_response = response  
            await self.process_response(response)

    async def process_response(self, ai_response):
        translated = translate_text(ai_response)  
        katakana = convert_to_katakana(translated)  
        romanized = romanji_translate(katakana)  
        print(f"\n{red}Sawa-sama EN{fr}: {blue}{ai_response}{fr}") 
        print(f"{red}Sawa-sama JP{fr}: {yellow}{katakana}{fr}")  
        print(f"{red}Sawa-sama JP{fr} ({cyan}Romanji{fr}): {cyan}{romanized}{fr}") 
        self.tts.generate_voicevox_audio(katakana) 
        await self.tts.play_audio(self.tts.wav_path) 
        
    def update_state(self, new_state):
        self.current_state = new_state

    def add_to_history(self, message):
        self.message_history.append(message)

    async def set_user_input(self, input_type, message):
        self.user_inputs[input_type] = message
        await self.process_input(message)  

    def clear_inputs(self):
        self.user_inputs.clear()

    async def handle_transcription(self, transcribed_text):
        self.add_to_history(transcribed_text)  
        await self.set_user_input('voice', transcribed_text)  


    async def start_recording(self):
        await record_audio(transcription_callback=self.handle_transcription)

    async def youtube_url_fetch(self, youtube_url):
        await fetch_and_handle_messages(youtube_url, self)  
        
global_state = GlobalState()
