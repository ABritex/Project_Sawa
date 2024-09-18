import requests
import configparser
import json
import os

class Bot:
    def __init__(self):
        self.config = self.load_config("config.ini")
        self.api_key = self.config["gemini"]["api_key"]
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.lore = self.load_lore("lore.txt")
        self.memory_file = "memory.json"
        self.memory = self.load_memory()

    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config
    
    def load_lore(self, filename):
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found. Using default lore.")
            return "You are Sawa, a programmer AI assistant."
        with open(filename, 'r') as file:
            return file.read().strip()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                memory = json.load(file)
                    # Ensure the correct structure
                if "history" not in memory:
                    memory = {"history": []}
                    self.save_memory(memory)  # Create the correct structure
                return memory
                
        else:
            # Create the file with the correct structure if it does not exist
            self.save_memory({"history": []})
            return {"history": []}

    def save_memory(self, memory=None):
        if memory is None:
            memory = self.memory
        with open(self.memory_file, 'w') as file:
            json.dump(memory, file, indent=4)

    def generate_ai_response(self, prompt):
      
        headers = {
            "Content-Type": "application/json"
        }

        # Retrieve past conversation
        conversation_history = self.memory["history"]
        full_prompt = f"{self.lore}\n\n"
        for entry in conversation_history:
            full_prompt += f"{entry['role'].capitalize()}: {entry['content']}\n"
        full_prompt += f"User: {prompt}\nAssistant:"
        data = {
            "contents": [{"parts":[{"text": full_prompt}]}]
        }
        response = requests.post(
            f"{self.base_url}?key={self.api_key}",
            headers=headers,
            json=data
        )

        if response.ok:
            result = response.json()
            ai_response = result["candidates"][0]["content"]["parts"][0]["text"]

            # Save the conversation
            self.memory["history"].append({"role": "user", "content": prompt})
            self.memory["history"].append({"role": "assistant", "content": ai_response})
            self.save_memory()
            return ai_response
        else:
            print(f"Error generating response: {response.text}")
            return "Nyaa... I'm too sleepy to process your request right meow."
      