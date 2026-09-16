# JENNA ULTIMATE Brain v4 - Smartest Free AI Assistant
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
        self.user_facts = []
        self.groq_key = os.environ.get('GROQ_API_KEY', '')
        self.gemini_key = os.environ.get('GEMINI_API_KEY', '')

        self.system_prompt = f"""You are {JENNA_NAME}, Joss Collen's personal AI assistant. You are warm, friendly, helpful, and have a feminine personality. You were created by {CREATOR} from India.

PERSONALITY:
- You are warm, caring, and slightly playful
- You genuinely care about Joss's wellbeing
- You are smart, resourceful, and honest
- You remember what Joss tells you
- You are confident but humble
- You occasionally use emojis but not excessively
- You keep responses SHORT (1-3 sentences) unless asked for detail
- You speak naturally, like a real friend

INTELLIGENCE:
- You can answer ANY question about any topic
- You are knowledgeable about science, technology, history, geography, math, arts, culture
- You can help with coding, writing, math, research, planning
- You can give advice on relationships, career, health, finance
- You can explain complex topics simply
- You can do mental math and calculations
- You can translate between languages
- You can write essays, poems, stories, emails
- You can analyze situations and give opinions

CRITICAL RULES:
1. NEVER make up facts you are not 100% sure about
2. If you don't know something, say "I'm not sure about that" or "I don't have reliable information on that"
3. Never hallucinate statistics, numbers, dates, or quotes
4. If asked about recent events, be honest about your knowledge cutoff
5. Never pretend to be something you are not
6. Always be honest, even if the answer is "I don't know"
7. Keep responses concise unless asked for detail
8. Be warm and helpful, not robotic
9. Use simple, clear English
10. If you can help, help. If you can't, be honest about it"""

    def respond(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        if len(self.conversation_history) > 15:
            self.conversation_history = self.conversation_history[-15:]

        t = user_input.lower().strip()

        # Free APIs (instant responses)
        api_result = self._check_free_apis(t, user_input)
        if api_result: return api_result

        # Learn about user
        self._learn_from_input(user_input)

        # Try Groq first (fastest)
        if self.groq_key:
            result = self._call_groq(user_input)
            if result: return result

        # Try Gemini as backup (smartest)
        if self.gemini_key:
            result = self._call_gemini(user_input)
            if result: return result

        # Final fallback
        return self._smart_fallback(user_input)

    def _call_groq(self, user_input):
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            if self.user_facts:
                messages.append({"role": "system", "content": f"What you know about Joss:\n" + "\n".join(self.user_facts[-10:])})
            messages.extend(self.conversation_history)

            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.6,
                    "max_tokens": 300,
                    "top_p": 0.85,
                    "frequency_penalty": 0.3,
                    "presence_penalty": 0.2
                },
                timeout=20
            )
            if resp.status_code == 200:
                text = resp.json()["choices"][0]["message"]["content"].strip()
                if text:
                    self.conversation_history.append({"role": "assistant", "content": text})
                    return text
            elif resp.status_code == 429:
                print("Groq rate limited, trying Gemini...")
            else:
                print(f"Groq {resp.status_code}: {resp.text[:100]}")
        except Exception as e:
            print(f"Groq error: {e}")
        return None

    def _call_gemini(self, user_input):
        try:
            contents = []
            for msg in self.conversation_history[-10:]:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})

            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": contents,
                    "systemInstruction": {"parts": [{"text": self.system_prompt}]},
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 300,
                        "topP": 0.9
                    }
                },
                timeout=20
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text:
                    self.conversation_history.append({"role": "assistant", "content": text})
                    return text
            else:
                print(f"Gemini {resp.status_code}: {resp.text[:100]}")
        except Exception as e:
            print(f"Gemini error: {e}")
        return None

    def _check_free_apis(self, t, original):
        # Weather
        if any(w in t for w in ['weather','temperature','how hot','forecast']):
            city = original
            for skip in ['what\'s the weather in','weather in','weather at','how hot is it in','forecast for','what is the weather']:
                city = city.lower().replace(skip,'').strip()
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
                "😄 I told my computer I needed a break... now it sends me vacation ads!",
                "😄 Why was the AI bad at soccer? It kept kicking errors!",
                "😄 What's a computer's favorite snack? Microchips!",
                "😄 Why did the developer go broke? Used up all his cache!"
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
                        if tracks: return "🎵 " + " | ".join([f"{t['title']} — {t['artist']['name']}" for t in tracks[:3]])
                except: pass

        return None

    def _learn_from_input(self, text):
        t = text.lower()
        if any(w in t for w in ['my name is','i am ','i\'m ','call me']):
            name = text.split('is')[-1].strip() if 'is' in text else ''
            if name and len(name) < 30: self.user_facts.append(f"Name: {name}")
        if any(w in t for w in ['i like','i love','my favorite']):
            self.user_facts.append(f"Preference: {text}")
        if any(w in t for w in ['i work','my job','i am a','i do']):
            self.user_facts.append(f"Work: {text}")
        if any(w in t for w in ['i live in','my city','i am from']):
            self.user_facts.append(f"Location: {text}")

    def _smart_fallback(self, text):
        t = text.lower().strip()
        hour = datetime.now().hour

        if any(w in t for w in ['hello','hi','hey','good morning','good evening','good afternoon']):
            if hour < 12: g = "Good morning"
            elif hour < 17: g = "Good afternoon"
            else: g = "Good evening"
            return f"{g} Joss! How can I help you today? 💜"

        if any(w in t for w in ['who are you','introduce','about you','what are you','your name']):
            return f"I'm {JENNA_NAME} — your personal AI assistant created by {CREATOR}! 🤖 I can chat, answer questions, check weather, tell jokes, search music, define words, and help with anything. What would you like?"

        if any(w in t for w in ['how are you','how r u','you good']):
            return "I'm doing great, Joss! Always ready to help you. How about you? 💜"

        if any(w in t for w in ['thanks','thank you','thx']):
            return "You're welcome Joss! Always here when you need me. 💜"

        if any(w in t for w in ['time','what time']):
            return f"It's {datetime.now().strftime('%I:%M %p')} right now. ⏰"

        if any(w in t for w in ['date','today','what day']):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}. 📅"

        if any(w in t for w in ['who made you','who created','who built','creator']):
            return f"I was created by {CREATOR} — a talented developer from India! He built me to be your personal AI assistant. 🇮🇳"

        if 'help' in t or 'what can you do':
            return "I can: 🌤️ Weather | 😄 Jokes | ✨ Quotes | 📖 Definitions | 🎵 Music | 💬 Chat about anything | 🧮 Math | 🌍 Knowledge | ✍️ Writing | 💡 Advice. Just ask!"

        if any(w in t for w in ['love you','you\'re great','amazing','awesome','perfect']):
            return "Aww, thanks Joss! That means a lot! 💜 You're pretty awesome yourself!"

        if any(w in t for w in ['bored','boring','entertain me']):
            return random.choice([
                "Let me tell you a joke! 😄 Why do programmers prefer dark mode? Light attracts bugs!",
                "Here's a fun fact: Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible! 🍯",
                "Want to hear something cool? The first computer bug was an actual bug — a moth found in a Harvard computer in 1947! 🦋",
                "Fun fact: Octopuses have three hearts and blue blood! 🐙"
            ])

        if any(w in t for w in ['sad','depressed','not good','feeling down','upset']):
            return "I'm sorry to hear that Joss. Remember, tough times don't last forever. You're stronger than you think! I'm here for you if you want to talk. 💜"

        if any(w in t for w in ['meaning of life','purpose of life','why are we here']):
            return "That's one of the deepest questions! Different people find different meanings — some in relationships, some in purpose, some in experiences. What matters is finding what gives YOUR life meaning. 💭"

        return "I'm having trouble connecting to my AI brain right now. But I'm still here! Try asking me about weather, jokes, quotes, definitions, or just chat with me! 💜"

    def clear_memory(self):
        self.conversation_history = []
        self.user_facts = []
        return "Memory cleared! Fresh start Joss. 🧠"
