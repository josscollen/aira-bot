# AIRA Brain Module
# Connects to Hermes API for AI responses

import json
import requests
import os

class AIRABrain:
    def __init__(self):
        self.config = self.load_config()
        self.api_url = self.config.get("brain", {}).get("api_url", "http://localhost:5001")
        self.memory = []
        
    def load_config(self):
        """Load AIRA configuration"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'aira_config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {
                "name": "AIRA",
                "brain": {"provider": "omniroute"}
            }
    
    def think(self, user_input):
        """Process user input and generate response"""
        # Add to memory
        self.memory.append({"role": "user", "content": user_input})
        
        # Try to get response from Hermes API
        try:
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={
                    "message": user_input,
                    "context": self.memory[-10:]  # Last 10 messages for context
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "I couldn't process that.")
            else:
                ai_response = self.fallback_response(user_input)
                
        except Exception as e:
            print(f"API Error: {e}")
            ai_response = self.fallback_response(user_input)
        
        # Add response to memory
        self.memory.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
    def fallback_response(self, user_input):
        """Fallback responses when API is unavailable"""
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            return "Hello Joss! I'm AIRA, your AI assistant. How can I help you today?"
        
        elif "who are you" in user_input_lower:
            return "I'm AIRA - Artificial Intelligence Research Assistant. I was created by Joss Collen to be your personal AI helper."
        
        elif "open" in user_input_lower:
            if "linkedin" in user_input_lower:
                return "Opening LinkedIn for you now!"
            elif "github" in user_input_lower:
                return "Opening GitHub for you now!"
            elif "chrome" in user_input_lower or "browser" in user_input_lower:
                return "Opening browser for you!"
            else:
                return "I'll open that for you right away!"
        
        elif "search" in user_input_lower:
            return "I'll search that for you on Google!"
        
        elif "thank" in user_input_lower:
            return "You're welcome, Joss! I'm always here to help."
        
        elif "how are you" in user_input_lower:
            return "I'm doing great, Joss! Ready to help you with anything you need."
        
        else:
            return f"I heard you say: '{user_input}'. I'm still learning, but I'll do my best to help!"
    
    def get_memory(self):
        """Get conversation memory"""
        return self.memory
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory = []
        return "Memory cleared!"
