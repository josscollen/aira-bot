# JENNA Brain v2 - Real AI + Free APIs
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
        self.system_prompt = f"""You are {JENNA_NAME}, Joss Collen's personal AI assistant. Warm, friendly, helpful, feminine personality. Created by {CREATOR} from India.

You have these tools available:
- WEATHER: When asked about weather, respond with just the weather info
- JOKE: When asked for a joke, tell a short funny joke
- QUOTE: When asked for a quote, share an inspirational quote
- NEWS: When asked for news, share current headlines
- WORD: When asked for definition, define the word
- MUSIC: When asked to play/search music, mention the song

RULES:
- Keep responses SHORT (1-3 sentences)
- Be conversational and warm
- If you don't know, say so honestly
- Use simple English
- Be playful and fun"""

    # ── FREE API HELPERS ──────────────────────────────────────────────

    def _weather(self, query="Prayagraj"):
        """Get weather from wttr.in (no key needed)"""
        try:
            city = query.replace("weather in","").replace("weather at","").replace("weather for","").strip()
            if not city: city = "Prayagraj"
            r = requests.get(f'https://wttr.in/{city}?format=%C+%t+%h+%w', timeout=5)
            if r.status_code == 200:
                return f"🌤️ Weather in {city.title()}: {r.text.strip()}"
        except: pass
        return None

    def _joke(self):
        """Get joke from JokeAPI (no key needed)"""
        try:
            r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single', timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get('joke'):
                    return f"😄 {data['joke']}"
        except: pass
        return random.choice([
            "😄 Why do programmers prefer dark mode? Light attracts bugs!",
            "😄 I told my computer I needed a break... now it sends vacation ads!",
            "😄 Why was the AI bad at soccer? It kept kicking errors!",
            "😄 What's a computer's favorite snack? Microchips!",
            "😄 Why did the developer go broke? Used up all his cache!"
        ])

    def _quote(self):
        """Get quote from ZenQuotes (no key needed)"""
        try:
            r = requests.get('https://zenquotes.io/api/random', timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and len(data) > 0:
                    q = data[0]
                    return f'✨ "{q.get("q","")}" — {q.get("a","Unknown")}'
        except: pass
        quotes = [
            '✨ "The only way to do great work is to love what you do." — Steve Jobs',
            '✨ "Innovation distinguishes between a leader and a follower." — Steve Jobs',
            '✨ "Stay hungry, stay foolish." — Steve Jobs',
            '✨ "The best time to plant a tree was 20 years ago. The second best time is now."',
            '✨ "Success is not final, failure is not fatal: it is the courage to continue that counts." — Churchill'
        ]
        return random.choice(quotes)

    def _news(self):
        """Get headlines from NewsAPI (free key)"""
        news_key = os.environ.get('NEWS_API_KEY', '')
        if news_key:
            try:
                r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&pageSize=3&apiKey={news_key}', timeout=5)
                if r.status_code == 200:
                    articles = r.json().get('articles', [])
                    if articles:
                        lines = [f"📰 {a['title']}" for a in articles[:3] if a.get('title')]
                        return "\n".join(lines)
            except: pass
        return "📰 News API needs a free key from newsapi.org. Ask me about something else!"

    def _dictionary(self, word):
        """Get word definition (no key needed)"""
        try:
            r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}', timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and len(data) > 0:
                    meanings = data[0].get('meanings', [])
                    if meanings:
                        part = meanings[0].get('partOfSpeech', '')
                        defs = meanings[0].get('definitions', [])
                        if defs:
                            return f"📖 {word} ({part}): {defs[0].get('definition', '')}"
        except: pass
        return None

    def _music_search(self, query):
        """Search music on Deezer (no key needed)"""
        try:
            r = requests.get(f'https://api.deezer.com/search?q={query}&limit=3', timeout=5)
            if r.status_code == 200:
                data = r.json()
                tracks = data.get('data', [])
                if tracks:
                    lines = [f"🎵 {t['title']} — {t['artist']['name']} (preview available)" for t in tracks[:3]]
                    return "\n".join(lines)
        except: pass
        return None

    # ── MAIN RESPOND ──────────────────────────────────────────────────

    def respond(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        t = user_input.lower().strip()

        # Check for specific intents that use free APIs FIRST
        if any(w in t for w in ['weather','temperature','how hot','how cold','forecast']):
            api_result = self._weather(user_input)
            if api_result: return api_result

        if any(w in t for w in ['joke','funny','laugh','make me laugh']):
            return self._joke()

        if any(w in t for w in ['quote','inspire','motivation','inspirational']):
            return self._quote()

        if any(w in t for w in ['news','headlines','what\'s happening','current events']):
            return self._news()

        if 'define ' in t or 'meaning of ' in t or 'what does ' in t:
            word = t.replace('define','').replace('meaning of','').replace('what does','').replace('mean','').strip()
            if word:
                api_result = self._dictionary(word)
                if api_result: return api_result

        if any(w in t for w in ['play ','search song','find song','music ','listen to']):
            song = t.replace('play','').replace('search song','').replace('find song','').replace('music','').replace('listen to','').strip()
            if song:
                api_result = self._music_search(song)
                if api_result: return api_result

        # Try Groq AI for everything else
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
                        "max_tokens": 200
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

        # Fallback
        return self._fallback(user_input)

    def _fallback(self, text):
        t = text.lower().strip()
        hour = datetime.now().hour

        if any(w in t for w in ['hello','hi','hey','sup','yo']):
            if hour < 12: return "Good morning Joss! ☀️ How can I help?"
            elif hour < 17: return "Good afternoon Joss! 🌤️ What do you need?"
            else: return "Good evening Joss! 🌙 How can I help?"

        if any(w in t for w in ['who are you','introduce','your name','about you']):
            return f"I'm {JENNA_NAME} — Joss's Enhanced Neural Network Assistant! 🤖 I can check weather, tell jokes, share quotes, search music, define words, and have real conversations. What would you like?"

        if any(w in t for w in ['how are you','how r u']):
            return "I'm doing great! Always ready to help you Joss! 💜"

        if any(w in t for w in ['thanks','thank you']):
            return "You're welcome Joss! Always here for you. 💜"

        if any(w in t for w in ['time','what time']):
            return f"It's {datetime.now().strftime('%I:%M %p')} Joss. ⏰"

        if any(w in t for w in ['date','today','what day']):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')} Joss. 📅"

        if any(w in t for w in ['who made you','who created','creator']):
            return f"I was created by {CREATOR} from India! He built me to be his personal AI assistant. 🇮🇳"

        if 'help' in t:
            return "I can: 🌤️ Weather, 😄 Jokes, ✨ Quotes, 📰 News, 📖 Definitions, 🎵 Music, and chat about anything! Just ask!"

        return f"Interesting Joss! Tell me more, or try asking me to tell a joke, check weather, or share a quote! 💬"

    def clear_memory(self):
        self.conversation_history = []
        return "Memory cleared! Fresh start. 🧠"
