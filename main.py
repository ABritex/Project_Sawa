# main.py
import sys
import keyboard  
from modules.globals import global_state
from colorama import Fore
import asyncio

red, green, blue, yellow, fr = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.RESET 

async def handle_terminal_input():
    while True:
        user_input = input(f"{green}You{fr}: ")
        if user_input.lower() == 'exit':
            return
        await global_state.set_user_input('terminal', user_input)  # Await the async function


async def handle_voice_input():
    print("Press and hold Right Shift to start voice input...")
    while True:
        if keyboard.is_pressed('RIGHT_SHIFT'):
            await global_state.start_recording()  
        if keyboard.is_pressed('ESC'):  
            print("Exited voice input mode.")
            break
        
async def handle_youtube_input():
    youtube_url = input("Enter the YouTube URL: ")
    if youtube_url:
        print("Listening to YouTube stream...")
        await global_state.youtube_url_fetch(youtube_url)  # Only pass youtube_url


async def main():
    print("Welcome to SawaSama AI Vtuber!")
    print(f"{blue}Choose an option{fr}:")
    print(f"{blue}1. Type your input{fr}")
    print(f"{blue}2. Voice input{fr}")
    print(f"{blue}3. YouTube chat input{fr}") 
    choice = input(f"{blue}Enter 1, 2, or 3{fr}: ").strip()
    if choice == "1":
        await handle_terminal_input()
    elif choice == "2":
        await handle_voice_input()     
    elif choice == "3":  
        await handle_youtube_input()   
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        
if __name__ == "__main__":
    asyncio.run(main()) 
