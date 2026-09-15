import json
import requests
import os

class AIRABrain:
    def __init__(self):
        self.memory = []
    
    def think(self, user_input):
        self.memory.append({"role": "user", "content": user_input})
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            response = "Hello Joss! I'm AIRA, your AI assistant. How can I help you today?"
        elif "who are you" in user_input_lower:
            response = "I'm AIRA - Artificial Intelligence Research Assistant, created by Joss Collen."
        elif "open linkedin" in user_input_lower:
            response = "Your LinkedIn: linkedin.com/in/shivam-prasad-mahto-1041192ab"
        elif "open github" in user_input_lower:
            response = "Your GitHub: github.com/josscollen"
        elif "what can you do" in user_input_lower:
            response = "I can chat with you, open websites, search Google, and help with tasks. On local mode I can also control your mouse, keyboard, and browser!"
        elif "search" in user_input_lower:
            query = user_input_lower.replace("search", "").replace("for", "").strip()
            response = f"Here's your search: https://www.google.com/search?q={query.replace(' ', '+')}"
        elif "thank" in user_input_lower:
            response = "You're welcome, Joss! Always here to help."
        elif "how are you" in user_input_lower:
            response = "I'm doing great, Joss! Ready to help."
        else:
            response = f"I heard: '{user_input}'. I'm AIRA, your AI assistant. What would you like me to do?"
        
        self.memory.append({"role": "assistant", "content": response})
        return response
    
    def get_memory(self):
        return self.memory
    
    def clear_memory(self):
        self.memory = []
        return "Memory cleared!"
