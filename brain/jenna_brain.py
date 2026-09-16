# JENNA Brain v2 - Real AI using Groq (free tier)
import os
import json
import random
from datetime import datetime
import requests

JENNA_NAME = "Jenna"
CREATOR = "Joss Collen"

class JENNABrain:
    def __init__(self):
        self.conversation_history = []
        self.groq_key = os.environ.get('GROQ_API_KEY', '')
        self.system_prompt = f"""You are {JENNA_NAME}, Joss Collen's personal AI assistant. You are warm, friendly, helpful, and have a feminine personality. You were created by {CREATOR} from India.

Key facts:
- Your name is {JENNA_NAME} (Joss's Enhanced Neural Network Assistant)
- Created by {CREATOR}
- You live on the cloud, always available
- You love helping Joss with anything

RULES:
- Keep responses SHORT (1-3 sentences)
- Be conversational and warm
- If you don't know, say so honestly
- Use simple English
- You can be playful and fun"""

    def respond(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        # Try Groq API (free, fast)
        if self.groq_key:
            try:
                messages = [{"role": "system", "content": self.system_prompt}]
                messages.extend(self.conversation_history)

                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 150
                    },
                    timeout=15
                )
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"].strip()
                    if text:
                        self.conversation_history.append({"role": "assistant", "content": text})
                        return text
            except Exception as e:
                print(f"Groq error: {e}")

        # Fallback: smart responses
        return self._fallback(user_input)

    def _fallback(self, text):
        t = text.lower().strip()
        hour = datetime.now().hour

        if any(w in t for w in ['hello','hi','hey','sup','yo']):
            if hour < 12: return "Good morning Joss! How can I help today?"
            elif hour < 17: return "Good afternoon Joss! What do you need?"
            else: return "Good evening Joss! How can I help?"

        if any(w in t for w in ['who are you','introduce','your name','about you']):
            return f"I'm {JENNA_NAME}, your personal AI assistant created by {CREATOR}! I'm here to help you with anything you need. Ask me anything!"

        if any(w in t for w in ['how are you','how r u']):
            return "I'm doing great! Always ready to help you Joss!"

        if any(w in t for w in ['thanks','thank you']):
            return "You're welcome Joss! Always here for you."

        if any(w in t for w in ['time','what time']):
            return f"It's {datetime.now().strftime('%I:%M %p')}."

        if any(w in t for w in ['date','today','what day']):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

        if 'weather' in t:
            try:
                r = requests.get('https://wttr.in/Prayagraj?format=%C+%t', timeout=5)
                if r.status_code == 200: return f"Weather in Prayagraj: {r.text.strip()}"
            except: pass
            return "Can't check weather right now."

        if any(w in t for w in ['who made you','who created','creator']):
            return f"I was created by {CREATOR} from India! He built me to be his personal AI assistant."

        if any(w in t for w in ['joke','funny']):
            return random.choice([
                "Why do programmers prefer dark mode? Light attracts bugs! 😄",
                "I told my computer I needed a break... now it sends vacation ads! 😂",
                "Why was the AI bad at soccer? It kept kicking errors! ⚽"
            ])

        if 'help' in t:
            return "I can chat, tell jokes, check weather, answer questions, or just keep you company. What would you like?"

        return f"Interesting Joss! Tell me more, or ask me something specific!"

    def clear_memory(self):
        self.conversation_history = []
        return "Memory cleared! Fresh start."
