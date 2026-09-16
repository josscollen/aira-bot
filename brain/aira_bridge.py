# AIRA Bridge API - Connects Telegram AIRA with Web Aura
# Allows both to talk to each other

import os
import json
import requests
from datetime import datetime

class AIRABridge:
    """Bridge between Telegram AIRA and Web Aura"""
    
    def __init__(self):
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        self.telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.aura_url = os.environ.get('AURA_URL', 'https://aira-bot.onrender.com')
        self.shared_memory = []
    
    def send_to_telegram(self, message):
        """Send message from Aura to Telegram AIRA"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": f"📱 From Aura:\n\n{message}",
            "parse_mode": "HTML"
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            return resp.status_code == 200
        except:
            return False
    
    def send_to_aura(self, message, password=None):
        """Send message from Telegram AIRA to Web Aura"""
        if not password:
            password = os.environ.get('AIRA_PASSWORD', 'Jossloveaira@123')
        try:
            resp = requests.post(f"{self.aura_url}/api/chat", 
                json={"message": message, "password": password},
                timeout=15)
            if resp.status_code == 200:
                return resp.json().get('response', 'No response')
            return f"Error: {resp.status_code}"
        except Exception as e:
            return f"Connection error: {str(e)}"
    
    def add_to_memory(self, sender, message, target):
        """Add message to shared memory"""
        self.shared_memory.append({
            "time": datetime.now().isoformat(),
            "sender": sender,
            "message": message,
            "target": target
        })
        # Keep last 50 messages
        if len(self.shared_memory) > 50:
            self.shared_memory = self.shared_memory[-50:]
    
    def get_memory(self):
        """Get shared memory"""
        return self.shared_memory

# Singleton
bridge = AIRABridge()
