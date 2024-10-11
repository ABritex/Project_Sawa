# run.py

import subprocess
    
def welcome_message():
    print(r"""
    /| 、 
  (˚ˎ 。7        Sawa AI
   |、˜〵          
  じしˍ,)ノ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
-----------------------------------------------------------------------
  Welcome to Sawa-sama, Your Virtual Companion!                          
-----------------------------------------------------------------------
- Sawa-sama is here to chat, learn, and entertain you in real time!
- Now powered with VoiceVox, LlaMa, Whisper AI, and more!
- Whether you're typing or chatting via voice, Sawa-sama's got you covered.

Commands:
- YouTube Mode: Paste a YouTube live stream link to start interacting with chat!
- Voice Mode: Start talking, and Sawa-sama will respond.
- Text Mode: Type your input, and get a reply instantly.
 
Enjoy your time with Sawa-sama, your AI-powered virtual friend!
-----------------------------------------------------------------------
""")

welcome_message()


if __name__ == "__main__":
    subprocess.run(["python", "main.py"])  # Adjust the command if you need to specify a virtual environment or specific Python version
