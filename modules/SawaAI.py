import configparser
import json
from groq import Groq  

# Load configuration
config = configparser.ConfigParser()
config.read("configs/config.ini")
LlaMa_API = config.get("LlaMa", "api_key") 
SawaAI = Groq(api_key=LlaMa_API)

def load_personality(filepath="configs/lore.txt"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "" 

def load_conversation_history(filepath="configs/conversation.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": []} 

def save_conversation_history(conversation, filepath="configs/conversation.json"):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=4)

def generate_prompt(conversation_history, personality):
    prompt = f"{personality}\n"
    for turn in conversation_history['history']:  # [-5:] Last 5 turns (customize as needed)
        role = turn["role"]
        content = turn["content"]
        prompt += f"{role.capitalize()}: {content}\n"
    return prompt

def generate_response(prompt):
    chat_completion = SawaAI.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",  
    )
    response = chat_completion.choices[0].message.content
    conversation = load_conversation_history()
    conversation["history"].append({"role": "assistant", "content": response})
    save_conversation_history(conversation)
    return response

def handle_input(user_input):
    personality = load_personality()
    conversation = load_conversation_history()
    conversation["history"].append({"role": "user", "content": user_input})
    save_conversation_history(conversation)
    prompt = generate_prompt(conversation, personality)
    ai_response = generate_response(prompt)
    
    return ai_response
