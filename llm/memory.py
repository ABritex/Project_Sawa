# memory.py
import json
import os
from datetime import datetime

class Memory:
    def __init__(self, memory_file="configs/conversation.json", max_entries=20):
        self.memory_file = memory_file
        self.max_entries = max_entries  
        self.ensure_memory_file()  

    def ensure_memory_file(self):
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as file:
                json.dump({"conversation": [], "youtube-chat": []}, file, indent=4)
        else:
            with open(self.memory_file, "r+") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
                if "conversation" not in data:
                    data["conversation"] = []
                if "youtube-chat" not in data:
                    data["youtube-chat"] = []
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

    def save_to_memory(self, input_text, llm_response, state="idle", injections=None):
        if injections is None:
            injections = []

        try:
            with open(self.memory_file, "r+") as file:
                data = json.load(file)
                conversation_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",  
                    "user_input": input_text,
                    "llm_response": llm_response,
                    "context": {
                        "state": state, 
                        "injections": injections  
                    }
                }
                data['conversation'].append(conversation_entry)
                data['conversation'] = data['conversation'][-self.max_entries:]
                file.seek(0) 
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.truncate()  
        except Exception as e:
            print(f"Error saving memory: {e}")
            
    def yt_chat_save_to_memory(self, user_name, user_chat):
        try:
            with open(self.memory_file, "r+") as file:
                data = json.load(file)
                chat_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "user_name": user_name,  
                    "user_chat": user_chat    
                }
                data['youtube-chat'].append(chat_entry)
                data['youtube-chat'] = data['youtube-chat'][-self.max_entries:]
                file.seek(0)  
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.truncate()  
        except Exception as e:
            print(f"Error saving YouTube chat memory: {e}")

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as file:
                return json.load(file).get('conversation', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading memory: {e}")
            return []
