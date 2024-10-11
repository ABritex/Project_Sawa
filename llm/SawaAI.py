from utils.api_loader import SawaAI 
from llm.memory import Memory
from datetime import datetime
memory = Memory()

def load_personality(filepath="configs/lore.txt"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def generate_prompt(conversation_history, personality):
    prompt = f"{personality}\n"
    for turn in conversation_history: 
        role = "User" if turn.get("user_input") else "Assistant" 
        content = turn.get("user_input") or turn.get("llm_response")  
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
    conversation = memory.load_memory()  
    conversation.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_input": user_input,
        "context": {"state": "engaged", "injections": []} 
    })
    prompt = generate_prompt(conversation, personality)
    ai_response = generate_response(prompt)
    conversation[-1]["llm_response"] = ai_response  
    memory.save_to_memory(user_input, ai_response)  
    return ai_response  