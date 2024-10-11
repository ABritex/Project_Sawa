# memory.py
import json
import os
from datetime import datetime

class Memory:
    def __init__(self, memory_file="configs/conversation.json", max_entries=20):
        self.memory_file = memory_file
        self.max_entries = max_entries  # Number of entries to keep
        self.ensure_memory_file()  # Ensure the memory file exists

    def ensure_memory_file(self):
        """Ensure that the conversation memory file exists, or create it."""
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
        """Save the conversation entry with timestamp, state, and optional injections."""
        if injections is None:
            injections = []

        try:
            with open(self.memory_file, "r+") as file:
                # Load existing data
                data = json.load(file)

                # Create conversation entry
                conversation_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",  # Save in UTC format
                    "user_input": input_text,
                    "llm_response": llm_response,
                    "context": {
                        "state": state,  # Current state of the conversation
                        "injections": injections  # Optional metadata or extra context
                    }
                }
                # Append the new entry
                data['conversation'].append(conversation_entry)

                # Limit conversation history to the last max_entries entries
                data['conversation'] = data['conversation'][-self.max_entries:]

                # Write back the updated conversation history
                file.seek(0)  # Move to the start of the file
                json.dump(data, file, ensure_ascii=False, indent=4)  # Write the updated data
                file.truncate()  # Remove any leftover data after the new JSON content
        except Exception as e:
            print(f"Error saving memory: {e}")
            
    def yt_chat_save_to_memory(self, user_name, user_chat):
        """Save YouTube chat user messages along with the user name to the conversation memory file."""
        try:
            with open(self.memory_file, "r+") as file:
                # Load existing data
                data = json.load(file)

                # Create entry for YouTube chat with user name and message
                chat_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "user_name": user_name,  # Save the user name
                    "user_chat": user_chat    # Save the user's message
                }

                # Append the new entry to the youtube-chat section
                data['youtube-chat'].append(chat_entry)

                # Limit YouTube chat history to the last max_entries entries
                data['youtube-chat'] = data['youtube-chat'][-self.max_entries:]

                # Write back the updated memory structure
                file.seek(0)  # Move to the start of the file
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.truncate()  # Remove any leftover data after the new JSON content
        except Exception as e:
            print(f"Error saving YouTube chat memory: {e}")



    def load_memory(self):
        """Load the conversation memory from the file."""
        try:
            with open(self.memory_file, "r") as file:
                return json.load(file).get('conversation', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading memory: {e}")
            return []
