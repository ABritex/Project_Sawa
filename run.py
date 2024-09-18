from bot import Bot
from speech import Speech
from colorama import Fore, Back, Style
r, g, b, fr = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.RESET
def main():
    bot = Bot()
    speech = Speech()
    while True:
        user_input = input(f"{b}You{fr}: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        gemini_response = bot.generate_ai_response(user_input)
        print(f"{r}SAWA-AI{fr}: {g}{gemini_response}{fr}")
        speech.generate_voicevox_audio(gemini_response)

if __name__ == "__main__":
    main()