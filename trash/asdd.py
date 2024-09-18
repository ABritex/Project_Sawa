import whisper

# Load the model
model = whisper.load_model("base")  # You can choose other models like "small", "medium", "large"

# Load the audio file
audio = whisper.load_audio("output.wav")

# Transcribe the audio
result = model.transcribe(audio)

# Print the transcribed text
print(result["text"])