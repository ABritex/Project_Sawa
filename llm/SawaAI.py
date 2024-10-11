import configparser
import json
from groq import Groq
from datetime import datetime
from llm.memory import Memory  # Import Memory class

# Load configuration
config = configparser.ConfigParser()
config.read("configs/config.ini")
LlaMa_API = config.get("LlaMa", "api_key")
SawaAI = Groq(api_key=LlaMa_API)

# Initialize memory
memory = Memory()

def load_personality(filepath="configs/lore.txt"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def generate_prompt(conversation_history, personality):
    prompt = f"{personality}\n"
    for turn in conversation_history:  # Loop through each conversation entry
        role = "User" if turn.get("user_input") else "Assistant"  # Determine the role based on user_input
        content = turn.get("user_input") or turn.get("llm_response")  # Get the appropriate content
        prompt += f"{role}: {content}\n"
    return prompt

def generate_response(prompt):
    chat_completion = SawaAI.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    response = chat_completion.choices[0].message.content
    return response

def handle_input(user_input):
    personality = load_personality()
    conversation = memory.load_memory()  # Load conversation history from memory

    # Update the conversation history with the user's input
    conversation.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_input": user_input,
        "context": {"state": "engaged", "injections": []}  # Include injections as needed
    })

    # Generate the prompt for the AI
    prompt = generate_prompt(conversation, personality)
    ai_response = generate_response(prompt)

    # Save the AI response in the conversation history
    conversation[-1]["llm_response"] = ai_response  # Update the last entry with AI response
    memory.save_to_memory(user_input, ai_response)  # Save the interaction to memory

    return ai_response  # Return the AI response


