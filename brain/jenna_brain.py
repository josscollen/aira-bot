# JENNA Brain v3 - Real AI + Free APIs + Smart fallback
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
- Created by {CREATOR}, a 21 year old from India
- You live on the cloud, always available
- You love helping Joss

RULES:
- Keep responses SHORT (1-3 sentences max)
- Be warm and conversational
- Use simple English
- Be helpful and sometimes playful"""

    def respond(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        t = user_input.lower().strip()

        # Free APIs (no key needed)
        if any(w in t for w in ['weather','temperature','how hot','forecast']):
            try:
                city = t.replace("weather in","").replace("weather at","").replace("weather for","").replace("what's the weather","").replace("weather","").strip() or "Prayagraj"
                r = requests.get(f'https://wttr.in/{city}?format=%C+%t+%h', timeout=5)
                if r.status_code == 200: return f"🌤️ Weather in {city.title()}: {r.text.strip()}"
            except: pass

        if any(w in t for w in ['joke','funny','laugh']):
            try:
                r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single', timeout=5)
                if r.status_code == 200:
                    j = r.json().get('joke','')
                    if j: return f"😄 {j}"
            except: pass
            return random.choice(["😄 Why do programmers prefer dark mode? Light attracts bugs!","😄 Why was the AI bad at soccer? It kept kicking errors!","😄 What's a computer's favorite snack? Microchips!"])

        if any(w in t for w in ['quote','inspire','motivation']):
            try:
                r = requests.get('https://zenquotes.io/api/random', timeout=5)
                if r.status_code == 200:
                    d = r.json()
                    if d: return f'✨ "{d[0]["q"]}" — {d[0]["a"]}'
            except: pass
            return '✨ "The only way to do great work is to love what you do." — Steve Jobs'

        if 'define ' in t or 'meaning of ' in t:
            word = t.replace('define','').replace('meaning of','').replace('what does','').replace('mean','').strip()
            if word:
                try:
                    r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=5)
                    if r.status_code == 200:
                        d = r.json()
                        if d and d[0].get('meanings'):
                            m = d[0]['meanings'][0]
                            defs = m.get('definitions',[])
                            if defs: return f"📖 {word} ({m.get('partOfSpeech','')}): {defs[0]['definition']}"
                except: pass

        if any(w in t for w in ['play ','search song','music ','listen to']):
            song = t.replace('play','').replace('search song','').replace('music','').replace('listen to','').strip()
            if song:
                try:
                    r = requests.get(f'https://api.deezer.com/search?q={song}&limit=2', timeout=5)
                    if r.status_code == 200:
                        tracks = r.json().get('data',[])
                        if tracks: return "🎵 " + " | ".join([f"{t['title']} — {t['artist']['name']}" for t in tracks[:2]])
                except: pass

        # Groq AI (real intelligence)
        if self.groq_key:
            try:
                messages = [{"role": "system", "content": self.system_prompt}]
                messages.extend(self.conversation_history)
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.3-70b-versatile", "messages": messages, "temperature": 0.7, "max_tokens": 200},
                    timeout=15
                )
                if resp.status_code == 200:
                    text = resp.json()["choices"][0]["message"]["content"].strip()
                    if text:
                        self.conversation_history.append({"role": "assistant", "content": text})
                        return text
                else:
                    print(f"Groq error {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                print(f"Groq error: {e}")

        # Fallback
        return self._fallback(user_input)

    def _fallback(self, text):
        t = text.lower().strip()
        hour = datetime.now().hour
        if any(w in t for w in ['hello','hi','hey']):
            return f"{'Good morning' if hour<12 else 'Good afternoon' if hour<17 else 'Good evening'} Joss! How can I help? 💜"
        if any(w in t for w in ['who are you','introduce','about you']):
            return f"I'm {JENNA_NAME} — your personal AI assistant created by {CREATOR}! I can chat, check weather, tell jokes, and help with anything. What would you like?"
        if any(w in t for w in ['how are you']): return "I'm great Joss! Always ready to help! 💜"
        if any(w in t for w in ['thanks','thank you']): return "You're welcome Joss! 💜"
        if any(w in t for w in ['time']): return f"It's {datetime.now().strftime('%I:%M %p')} ⏰"
        if any(w in t for w in ['date','today']): return f"Today is {datetime.now().strftime('%A, %B %d, %Y')} 📅"
        if any(w in t for w in ['who made','creator','built you']): return f"I was created by {CREATOR} from India! 🇮🇳"
        return "I'm having trouble connecting to my AI brain right now. Try again in a moment, or ask me about weather, jokes, quotes, or definitions! 💜"

    def clear_memory(self):
        self.conversation_history = []
        return "Memory cleared! Fresh start. 🧠"
