# Installation

```
pip install -r requirements.txt
```

## Used:

- [Voicevox Docker](https://hub.docker.com/r/voicevox/voicevox_engine) or open in [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb)
- VB Audio Or [VTC Desktop Audio](https://lualucky.itch.io/vts-desktop-audio-plugin?download) (Optional)
- [VTube Studio](https://store.steampowered.com/app/1325860/VTube_Studio/)
- Whisper AI
- [Deeplx](https://github.com/OwO-Network/DeepLX)

## API's

- [LlaMa](https://console.groq.com)

# File Directory

```
SawaSama/
├─ configs/
│   ├─ lore.txt                 # AI personality configuration
│   ├─ config.ini               # API keys and other configuration settings
│   └─ conversation.json        # History of AI chats, saved as user and assistant roles
├─ modules/
│   ├─ globals.py               # Will call all the modules
│   ├─ katakana.py              # Handles Katakana conversion for natural Japanese speech
│   ├─ SawaAI.py                # The AI responsible for input handling
│   ├─ speech.py                # VoiceVox engine, plays audio output.wav
│   └─ translate.py             # Handles translation (Google Translate, Deeplx)
├─ sounds/
│   ├─ output.wav               # Audio produced by Speech.py
│   └─ input.wav                # Audio produced by run.py using pyaudio
├─ utils/
│   ├─ subtitle.py              # Handles writing AI responses to text files for OBS
│   ├─ streampet_msg_until.py   # StreamPet simulator message utility
│   └─ SawaAI_msg_until.py      # Utility to skip AI chat history
├─ requirements.txt             # Python package dependencies
├─ run.py                       # Script for user input conversation with the AI
├─ twitchapi.py                 # For Twitch chat + voice input interaction
├─ ytapi.py                     # For YouTube chat + voice input interaction
├─ stream_pet.py                # VPet simulator functionality
├─ output.txt                   # Text file for AI's English response (read by OBS)
├─ chat.txt                     # Text file for AI's English response (read by OBS)
└─ README.md                    # Project documentation
```
