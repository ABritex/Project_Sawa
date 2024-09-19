import asyncio
from modules.SawaAI import handle_input
from modules.translate import translate_text
from modules.katakana import apply_katakana
from modules.speech import Speech
from utils.subtitles import generate_subtitle  
from colorama import Fore, Back, Style

red, green, blue, yellow, fr = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RESET 

def process_input(user_input: str):
    speech = Speech()
    ai_response = handle_input(user_input)
    japanese_response = translate_text(ai_response)
    katakana_text = apply_katakana(japanese_response)
    print(f"{red}Sawa-sawa EN{fr}: {red}{ai_response}{fr}")
    print(f"{yellow}Sawa-sawa JP{fr}: {yellow}{katakana_text}{fr}")
    
    result_id = ai_response 
    generate_subtitle(user_input, result_id) 

    speech.generate_voicevox_audio(katakana_text)
    asyncio.run(speech.play_audio(speech.wav_path))
    
    with open("output.txt", "w", encoding="utf-8") as outfile:
        outfile.write("") 
    with open("chat.txt", "w", encoding="utf-8") as outfile:
        outfile.write("")  
    
    
    print(f"{blue}Finished playing. Start Your input again{fr}")

    return katakana_text