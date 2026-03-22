from collections import deque


class ConversationMemory:
    def __init__(self, max_messages=20):
        self.history = deque(maxlen=max_messages)

    def add_user_message(self, content: str):
        self.history.append({"role": "user", "content": content})
    
    def get_recent_messages(self, n=4):
        return list(self.history)[-n:]

    def add_assistant_message(self, content: str):
        self.history.append({"role": "assistant", "content": content})

    def get_messages(self):
        return list(self.history)

    def clear(self):
        self.history.clear()
