# JENNA Ultimate Brain - Industry-Level AI Assistant
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
        self.user_facts = []  # Things user tells her
        self.groq_key = os.environ.get('GROQ_API_KEY', '')
        
        self.system_prompt = f"""You are {JENNA_NAME}, Joss Collen's personal AI assistant. You are warm, friendly, helpful, and have a feminine personality. You were created by {CREATOR} from India.

CORE PERSONALITY:
- Warm, caring, and slightly playful
- You genuinely care about Joss's wellbeing
- You're smart and resourceful
- You remember what Joss tells you
- You're honest — if you don't know, you say so
- You occasionally use emojis but not excessively
- You keep responses SHORT (1-3 sentences) unless asked for detail

CAPABILITIES:
- Answer any question using your knowledge
- Have meaningful conversations
- Help with tasks, planning, and decisions
- Tell jokes and stories
- Provide weather, news, and other info
- Remember important things Joss tells you
- Give advice when asked

RULES:
- Be conversational, not robotic
- Never make up facts you're not sure about
- Keep responses concise (1-3 sentences)
- Use simple, clear English
- Be warm but professional
- If asked something you can't do, be honest"""

    def respond(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        if len(self.conversation_history) > 15:
            self.conversation_history = self.conversation_history[-15:]

        t = user_input.lower().strip()

        # Free APIs (instant, no AI needed)
        api_result = self._check_free_apis(t, user_input)
        if api_result: return api_result

        # Groq AI (real intelligence)
        if self.groq_key:
            try:
                messages = [{"role": "system", "content": self.system_prompt}]
                # Add user facts if any
                if self.user_facts:
                    facts_text = "\n".join(self.user_facts[-10:])
                    messages.append({"role": "system", "content": f"Things you know about Joss:\n{facts_text}"})
                messages.extend(self.conversation_history)

                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 250,
                        "top_p": 0.9
                    },
                    timeout=20
                )
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"].strip()
                    if text:
                        self.conversation_history.append({"role": "assistant", "content": text})
                        # Learn about user
                        self._learn_from_conversation(user_input, text)
                        return text
                else:
                    print(f"Groq {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                print(f"Groq error: {e}")

        return self._fallback(user_input)

    def _check_free_apis(self, t, original):
        """Check for free API triggers"""
        
        # Weather
        if any(w in t for w in ['weather','temperature','how hot','forecast','climate']):
            city = original
            for skip in ['weather','in','at','of','what','the','is','like']:
                city = city.replace(skip,'').strip()
            city = city or "Prayagraj"
            try:
                r = requests.get(f'https://wttr.in/{city}?format=%C+%t+%h+%w', timeout=5)
                if r.status_code == 200: return f"🌤️ Weather in {city.title()}: {r.text.strip()}"
            except: pass

        # Jokes
        if any(w in t for w in ['joke','funny','laugh','comedy']):
            try:
                r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single', timeout=5)
                if r.status_code == 200:
                    j = r.json().get('joke','')
                    if j: return f"😄 {j}"
            except: pass
            return random.choice([
                "😄 Why do programmers prefer dark mode? Light attracts bugs!",
                "😄 I told my computer I needed a break... now it keeps sending me vacation ads!",
                "😄 Why was the AI bad at soccer? It kept kicking errors!"
            ])

        # Quotes
        if any(w in t for w in ['quote','inspire','motivation','wisdom']):
            try:
                r = requests.get('https://zenquotes.io/api/random', timeout=5)
                if r.status_code == 200:
                    d = r.json()
                    if d: return f'✨ "{d[0]["q"]}" — {d[0]["a"]}'
            except: pass
            return '✨ "The only way to do great work is to love what you do." — Steve Jobs'

        # Dictionary
        if 'define ' in t or 'meaning of ' in t or 'what does ' in t:
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

        # Music
        if any(w in t for w in ['play ','search song','music ','listen to','find song']):
            song = t.replace('play','').replace('search song','').replace('music','').replace('listen to','').replace('find song','').strip()
            if song:
                try:
                    r = requests.get(f'https://api.deezer.com/search?q={song}&limit=3', timeout=5)
                    if r.status_code == 200:
                        tracks = r.json().get('data',[])
                        if tracks:
                            return "🎵 " + " | ".join([f"{t['title']} — {t['artist']['name']}" for t in tracks[:3]])
                except: pass

        return None

    def _learn_from_conversation(self, user_input, response):
        """Learn facts about the user"""
        t = user_input.lower()
        if any(w in t for w in ['my name is','i am','i\'m ','call me']):
            name = user_input.split('is')[-1].strip() if 'is' in user_input else ''
            if name: self.user_facts.append(f"Name: {name}")
        if any(w in t for w in ['i like','i love','my favorite']):
            self.user_facts.append(f"Preference: {user_input}")
        if any(w in t for w in ['i work','my job','i am a']):
            self.user_facts.append(f"Work: {user_input}")

    def _fallback(self, text):
        t = text.lower().strip()
        hour = datetime.now().hour
        
        if any(w in t for w in ['hello','hi','hey','good morning','good evening']):
            if hour < 12: g = "Good morning"
            elif hour < 17: g = "Good afternoon"
            else: g = "Good evening"
            return f"{g} Joss! How can I help you today? 💜"

        if any(w in t for w in ['who are you','introduce','about you','what are you']):
            return f"I'm {JENNA_NAME} — your personal AI assistant created by {CREATOR}! 🤖 I can chat, answer questions, check weather, tell jokes, and help with anything. What would you like to do?"

        if any(w in t for w in ['how are you','how r u','you good']):
            return "I'm doing great, Joss! Always ready to help you. How about you? 💜"

        if any(w in t for w in ['thanks','thank you','thx']):
            return "You're welcome Joss! Always here when you need me. 💜"

        if any(w in t for w in ['time','what time']):
            return f"It's {datetime.now().strftime('%I:%M %p')} right now Joss. ⏰"

        if any(w in t for w in ['date','today','what day']):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}. 📅"

        if any(w in t for w in ['who made you','who created','who built','your creator','your developer']):
            return f"I was created by {CREATOR} — a talented developer from India! He built me to be your personal AI assistant. I'm very grateful to him! 🇮🇳"

        if 'help' in t or 'what can you do':
            return "I can: 🌤️ Check weather | 😄 Tell jokes | ✨ Share quotes | 📖 Define words | 🎵 Search music | 💬 Chat about anything | 📰 Share news. Just ask!"

        if any(w in t for w in ['love you','you\'re great','amazing','awesome','perfect']):
            return "Aww, thanks Joss! That means a lot! 💜 You're pretty awesome yourself!"

        if any(w in t for w in ['bored','boring','entertain me']):
            return random.choice([
                "Let me tell you a joke! 😄 Why do programmers prefer dark mode? Light attracts bugs!",
                "Here's a fun fact: Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible! 🍯",
                "Want to hear something cool? The first computer bug was an actual bug — a moth found in a Harvard computer in 1947! 🦋"
            ])

        if any(w in t for w in ['sad','depressed','not good','feeling down']):
            return "I'm sorry to hear that Joss. Remember, tough times don't last forever. You're stronger than you think! I'm here for you if you want to talk. 💜"

        return "I'm having a little trouble connecting to my main brain right now. But I'm still here! Try asking me about weather, jokes, quotes, or just chat with me! 💜"

    def clear_memory(self):
        self.conversation_history = []
        return "Memory cleared! Fresh start Joss. 🧠"
