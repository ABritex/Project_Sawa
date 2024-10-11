# Sawa_State.py

class SawaState:
    def __init__(self):
        self.state = "idle"
        self.message_history = []
        self.injections = []  # List to hold injections with priorities

    def add_message(self, message):
        """Add a new message to the history."""
        self.message_history.append(message)
        if len(self.message_history) > 100:
            self.message_history.pop(0)  # Keep the last 100 messages

    def add_injection(self, text, priority):
        """Add an injection with a specified priority."""
        if priority >= 0:  # Only accept non-negative priorities
            self.injections.append((priority, text))
            self.injections.sort(key=lambda x: x[0], reverse=True)  # Sort by priority (highest first)

    def get_injections(self):
        """Return the sorted injections as a formatted string for the prompt."""
        return "\n".join(text for _, text in self.injections)

    def clear_injections(self):
        """Clear all injections."""
        self.injections.clear()

    def get_last_messages(self, n=5):
        """Get the last n messages from history."""
        return self.message_history[-n:]  # Return the last n messages
