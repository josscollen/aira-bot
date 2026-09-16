# JENNA Brain - No external API dependency
# Uses built-in responses + smart pattern matching

import os
import json
import random
from datetime import datetime

class JENNABrain:
    def __init__(self):
        self.memory = []
        self.creator = "Joss Collen"
        self.user_name = "Joss"
        self.context = []
        
        # Smart response patterns
        self.responses = {
            "greeting": [
                f"Hey {self.user_name}! What's up?",
                f"Hi {self.user_name}! How can I help?",
                f"Hello {self.user_name}! What do you need?",
                f"Hey! I'm here and ready.",
            ],
            "how_are_you": [
                "I'm doing great, thanks for asking!",
                "All systems running smooth!",
                "Pretty good! Ready to help you.",
            ],
            "who_are_you": [
                f"I'm JENNA - Joss's Enhanced Neural Network Assistant. I'm your personal AI, built by {self.creator}.",
                f"I'm JENNA. Your personal AI assistant, created by {self.creator}. I'm here to help you with anything you need.",
            ],
            "what_can_you_do": [
                "I can chat with you, answer questions, help with tasks, search the web, set reminders, and save notes. Just ask me anything!",
                "I'm your AI assistant - I can help with research, answer questions, manage reminders, take notes, and have conversations. What would you like?",
            ],
            "thanks": [
                "You're welcome!",
                "Anytime!",
                "Happy to help!",
                "No problem!",
            ],
            "bye": [
                "See you later!",
                "Bye! Come back anytime.",
                "Talk to you soon!",
            ],
            "help": [
                "Sure, I'm here to help! What do you need?",
                "What can I help you with?",
                "Tell me what you need and I'll do my best.",
            ],
            "name": [
                f"My name is JENNA - {self.creator}'s personal AI assistant.",
                f"I'm JENNA. {self.creator} built me to be his AI research assistant.",
            ],
            "time": [
                f"It's {datetime.now().strftime('%I:%M %p')} right now.",
                f"The current time is {datetime.now().strftime('%I:%M %p on %B %d, %Y')}.",
            ],
            "weather": [
                "I don't have weather data yet, but I can help you check it online!",
                "I can't check weather directly, but you can ask me to search for it!",
            ],
            "joss": [
                f"You're {self.creator}, my creator! How can I help you?",
                f"That's you! {self.creator} - my creator and best friend.",
            ],
            "default": [
                "That's interesting! Tell me more.",
                "I understand. What else would you like to know?",
                "Got it! Is there anything specific I can help with?",
                "I see. Let me know if you need anything!",
                "Thanks for sharing! What else?",
                "I'm listening. What else is on your mind?",
                "Interesting! Tell me more about that.",
            ],
        }
        
        # Keywords to detect intent
        self.keywords = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening", "good night", "sup", "yo"],
            "how_are_you": ["how are you", "how r u", "whats up", "what's up", "how you doing", "you good"],
            "who_are_you": ["who are you", "what are you", "your name", "tell me about yourself"],
            "what_can_you_do": ["what can you do", "capabilities", "features", "what do you do", "help me"],
            "thanks": ["thank", "thanks", "thx", "appreciate", "ty"],
            "bye": ["bye", "goodbye", "see you", "later", "gtg", "gotta go"],
            "help": ["help", "assist", "support", "need help"],
            "name": ["your name", "jenna", "what's your name"],
            "time": ["time", "what time", "current time", "what's the time"],
            "weather": ["weather", "temperature", "forecast", "rain", "sun"],
            "joss": ["joss", "joss collen", "shivam", "who am i", "who made you"],
        }
    
    def detect_intent(self, message):
        msg = message.lower().strip()
        
        for intent, words in self.keywords.items():
            for word in words:
                if word in msg:
                    return intent
        
        return "default"
    
    def think(self, message):
        """Process message and return response"""
        # Add to memory
        self.memory.append({
            "time": datetime.now().isoformat(),
            "user": message,
            "type": "user"
        })
        
        # Detect intent
        intent = self.detect_intent(message)
        
        # Get response
        responses = self.responses.get(intent, self.responses["default"])
        response = random.choice(responses)
        
        # Add to memory
        self.memory.append({
            "time": datetime.now().isoformat(),
            "jenna": response,
            "type": "jenna"
        })
        
        return response
    
    def get_memory(self):
        return self.memory[-20:]  # Last 20 messages
    
    def clear_memory(self):
        self.memory = []
