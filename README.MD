# Installation

```
pip install -r requirements.txt
```

create a "config.ini" in /configs/ directory

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
├─ llm/
│   ├─ SawaAI.py
│   └─ Sawa_State.py
├─ configs/
│   ├─ lore.txt
│   ├─ config.ini
│   └─ conversation.json
├─ modules/
│   ├─ globals.py
│   ├─ katakana.py
│   ├─ romanize.py
│   ├─ speech.py
│   ├─ youtube.py
│   └─ translate.py
├─ sounds/
│   ├─ output.wav
│   └─ input.wav
├─ utils/
│   └─  subtitle.py
├─ requirements.txt
├─ main.py
├─ run.py
├─ output.txt
├─ chat.txt
└─ README.md
```

I want to create an AI Vtuber program code using python, for that i'll use LlaMa, VoiceVox, DeepLx, Whisper AI, OBS, Pychat, Vtuber Studio and etc.

Flow of the system

"1. Run";
run.py will run the -> main.py this has a 3 user input which is 1. terminal user input, 2. voice input (this is process by holding shift), 3. youtube + voice input auto.

"2. globals calls"
this will be the caller inside of the modules/,
main.py -> globals -> "3. llm state".

"3. llm state"
sawa_state.py -> chat_handler.py -. "4. llm process"
here will is the process of the chat/user/host.
Checks in sawa_state checks if its idling, chat_handler will prorcess the chats
Represents some text to be injected into the LLM prompt.
Injections are added to the prompt from lowest to highest priority, with the highest being at the end.
Text is the text to be injected.
Priority is a positive integer. Injections with negative priority will be ignored.

examples:
System Prompt Priority: 10
Message History: 50
TwitcTh Chat: 100

"4. llm process"
memory.py -> sawaai.py -> return "5. global process"
periodically, check if at least 20 new messages have been sent, and if so, generate 3 question-answer pairs
to be stored into memory.
This is a technique called reflection. You essentially ask the AI what information is important in the recent
conversation, and it is converted into a memory so that it can be recalled later.
memory.py will handle the conversation.json, while sawaai.py is the AI will process the message,
also checks the lore.txt for the personality.

"5. global process"
sawaai.py -> globals.py
will be translate.py, katakana.py, romanize.py and tts.py
process after getting the returned prompt from the llm it wll get back to globals then will process the translation -> katakana -> romanize -> tts

Does it works like if, for example a multiple user and me as a the host of the live stream ofc there will be a multiple user will chat and me as a speak, can it process like getting those mutliple messages then it will process the topics before the AI response? or like nGiven only the information above, what are 3 most salient high level questions we can answer about the subjects in the conversation? Separate each question and answer pair with \"{qa}\", and only output the question and answer, no explanations

what if a user

what if
user 1: hi sawa
user 2: how are youu
host (me): what should i do
user 3: damn son
user 1: sawa pick me
