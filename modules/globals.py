from modules.audio import record_audio
from modules.translate import translate_text  # Adjust the import based on your structure
from modules.katakana import convert_to_katakana  # Adjust the import based on your structure
from modules.romanize import romanji_translate  # Adjust the import based on your structure
from modules.tts import TTS  # Import your TTS class
from modules.youtube import fetch_and_handle_messages  # Import your function
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
        self.sawa_state = SawaState()  # Initialize SawaState
        self.chat_handler = ChatHandler()  # Initialize ChatHandler
        self.tts = TTS()
        self.memory = Memory()  # Initialize memory

    async def handle_input_event(input_text):
        await global_state.process_input(input_text)

    async def process_input(self, input_text, source=None):
        """Process input by delegating to handle_input."""
        # Check the source before processing
        if source != 'youtube_chat':
            response = handle_input(input_text)  # Use the handle_input to get a response
            self.llm_response = response  # Store the AI response for later use
            await self.process_response(response)  # Call process_response to handle the AI response

    async def process_response(self, ai_response):
        translated = translate_text(ai_response)  
        katakana = convert_to_katakana(translated)  
        romanized = romanji_translate(katakana)  
        print(f"\n{red}Sawa-sama EN{fr}: {blue}{ai_response}{fr}")  # Print the English response
        print(f"{red}Sawa-sama JP{fr}: {yellow}{katakana}{fr}")  # Print the Japanese katakana response
        print(f"{red}Sawa-sama JP{fr} ({cyan}Romanji{fr}): {cyan}{romanized}{fr}")  # Print the romanized response
        self.tts.generate_voicevox_audio(katakana)  # Generate the audio from katakana
        await self.tts.play_audio(self.tts.wav_path) 
        
    def update_state(self, new_state):
        self.current_state = new_state

    def add_to_history(self, message):
        # Your logic to add the message to history
        self.message_history.append(message)

    async def set_user_input(self, input_type, message):
        self.user_inputs[input_type] = message
        await self.process_input(message)  # Await the async process_input
    # Process input

    def clear_inputs(self):
        self.user_inputs.clear()

    async def handle_transcription(self, transcribed_text):
        self.add_to_history(transcribed_text)  
        await self.set_user_input('voice', transcribed_text)  # Update user input to use transcribed text


    async def start_recording(self):
        await record_audio(transcription_callback=self.handle_transcription)

    async def youtube_url_fetch(self, youtube_url):
        await fetch_and_handle_messages(youtube_url, self)  
        
# Instantiate a global state object
global_state = GlobalState()
