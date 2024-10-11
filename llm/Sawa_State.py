class SawaState:
    def __init__(self):
        self.state = "idle"
        self.message_history = []
        self.injections = [] 

    def add_message(self, message):
        self.message_history.append(message)
        if len(self.message_history) > 100:
            self.message_history.pop(0) 

    def add_injection(self, text, priority):
        if priority >= 0: 
            self.injections.append((priority, text))
            self.injections.sort(key=lambda x: x[0], reverse=True)

    def get_injections(self):
        return "\n".join(text for _, text in self.injections)

    def clear_injections(self):
        self.injections.clear()

    def get_last_messages(self, n=5):
        return self.message_history[-n:] 
