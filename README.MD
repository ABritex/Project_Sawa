# Installation

```
pip install -r requirements.txt
```

create a ".env" in /configs/ directory

```
# Others
# GEMINI_API_KEY=
# OBS_HOST=
# OBS_PORT=
# OBS_PASSWORD=
# YOUTUBE_API_KEY=

# ENV
LLAMA_API_KEY=
DEEPLX_API_URL=
VOICEVOX_URL=
SPEAKER_ID=

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
├─ llm/
│   ├─ SawaAI.py
│   └─ Sawa_State.py
├─ configs/
│   ├─ lore.txt
│   ├─ .env
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
│   ├─ env_loader.py
│   └─ subtitle.py
├─ requirements.txt
├─ main.py
├─ run.py
├─ output.txt
├─ chat.txt
└─ README.md
```
