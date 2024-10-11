import pytchat
import re
import time
from collections import defaultdict, deque
from utils.chat_handler import ChatHandler

def extract_video_id(youtube_url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

class SpamHandler:
    def __init__(self, message_limit=5, time_window=10):
        self.message_limit = message_limit
        self.time_window = time_window
        self.user_message_timestamps = defaultdict(deque)

    def is_spammer(self, user):
        current_time = time.time()
        timestamps = self.user_message_timestamps[user]
        while timestamps and current_time - timestamps[0] > self.time_window:
            timestamps.popleft()
        timestamps.append(current_time)

        return len(timestamps) > self.message_limit

class MessageHandler:
    def __init__(self, chat_handler, global_state):
        self.spam_handler = SpamHandler()
        self.chat_handler = chat_handler
        self.global_state = global_state 
        self.messages = [] 

    def process_message(self, user, message):
        if self.spam_handler.is_spammer(user):
            print(f"Ignoring message from spammer {user}")
            return None

        self.messages.append((user, message))  
        self.global_state.memory.yt_chat_save_to_memory(user, message)
        self.chat_handler.check_and_reflect(self.messages, self.global_state)
        return None

def fetch_and_handle_messages(youtube_url, global_state):
    video_id = extract_video_id(youtube_url)
    chat = pytchat.create(video_id=video_id)
    chat_handler = ChatHandler()
    handler = MessageHandler(chat_handler, global_state)

    print(f"Monitoring YouTube chat for video: {youtube_url}")
    while chat.is_alive():
        for c in chat.get().items:
            user = c.author.name
            message = c.message
            response = handler.process_message(user, message)
            if response:
                print(f"Response to {user}: {response}")
