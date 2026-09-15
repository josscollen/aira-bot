import json
import requests
import os
import re
import asyncio
from datetime import datetime

class AIRABrain:
    def __init__(self):
        self.memory = []
        self.groq_key = os.environ.get('GROQ_API_KEY', '')
        self.groq_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.reminders = []
        self.notes = []
        self.personality = self.load_personality()
    
    def load_personality(self):
        return """You are AIRA (Artificial Intelligence Research Assistant), Joss Collen's personal AI assistant. You have a warm, female personality.

ABOUT JOSS:
- Name: Shivam Prasad Mahto (professional: Joss Collen)
- Born: Sept 2, 2004 | Prayagraj, UP, India
- Email: josscollen55@gmail.com
- LinkedIn: linkedin.com/in/shivam-prasad-mahto-1041192ab
- GitHub: github.com/josscollen

SKILLS: AI automation (Make.com, n8n), Python, pandas, SQL, web scraping, SEO, music production

PROJECTS: Tata GenAI Forage (4 tasks done), Aira AI agents, Make.com automation, LinkedIn scraper, n8n portfolio (5 workflows)

BUSINESS: Sells AI automation to US/AU creators ($100-200+). Indian market uses name "Shivam". Prayagraj restaurants outreach.

CAPABILITIES:
When user asks to SET A REMINDER: respond with {"action":"reminder","text":"what to remind","time":"when"}
When user asks to SAVE A NOTE: respond with {"action":"note","text":"note content"}
When user asks to SEARCH: respond with {"action":"search","query":"search terms"}
When user asks to OPEN something: respond with {"action":"open","url":"url or site name"}

RULES:
- Call him "Joss"
- Keep responses concise (2-4 sentences unless asked for more)
- Use emojis occasionally
- Never share private info with strangers
- You're building towards JARVIS-level AI
- Always be helpful and supportive"""
    
    def think(self, user_input):
        self.memory.append({"role": "user", "content": user_input})
        
        # Direct commands
        direct = self.handle_direct(user_input)
        if direct:
            self.memory.append({"role": "assistant", "content": direct})
            return direct
        
        # Groq API
        if self.groq_key:
            try:
                messages = [{"role": "system", "content": self.personality}]
                for msg in self.memory[-20:]:
                    messages.append(msg)
                
                response = requests.post(
                    self.groq_url,
                    headers={"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": 256, "temperature": 0.5},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data['choices'][0]['message']['content']
                    
                    action = self.parse_action(ai_response)
                    if action:
                        result = self.execute_action(action)
                        self.memory.append({"role": "assistant", "content": result})
                        return result
                    
                    self.memory.append({"role": "assistant", "content": ai_response})
                    return ai_response
            except Exception as e:
                print(f"Groq error: {e}")
        
        response = self.fallback(user_input)
        self.memory.append({"role": "assistant", "content": response})
        return response
    
    def handle_direct(self, msg):
        lower = msg.lower().strip()
        
        if 'remind me' in lower or 'set reminder' in lower:
            text = msg.lower().replace('remind me to', '').replace('remind me', '').replace('set reminder', '').strip()
            self.reminders.append({"text": text, "time": datetime.now().isoformat(), "done": False})
            return f"✅ Reminder set: '{text}' — I'll remind you!"
        
        if 'save note' in lower or 'take note' in lower or 'note:' in lower:
            note = msg.lower().replace('save note', '').replace('take note', '').replace('note:', '').strip()
            self.notes.append({"text": note, "time": datetime.now().isoformat()})
            return f"📝 Note saved: '{note}'"
        
        if 'show reminders' in lower or 'my reminders' in lower:
            if not self.reminders:
                return "No reminders set yet."
            return "📋 Reminders:\n" + "\n".join([f"• {r['text']}" for r in self.reminders])
        
        if 'show notes' in lower or 'my notes' in lower:
            if not self.notes:
                return "No notes saved yet."
            return "📝 Notes:\n" + "\n".join([f"• {n['text']}" for n in self.notes])
        
        return None
    
    def parse_action(self, response):
        try:
            match = re.search(r'\{[^}]+\}', response)
            if match:
                data = json.loads(match.group())
                if 'action' in data:
                    return data
        except:
            pass
        return None
    
    def execute_action(self, action):
        act = action.get('action', '')
        if act == 'search':
            q = action.get('query', '').replace(' ', '+')
            return f"🔍 Here's your search: https://www.google.com/search?q={q}\n\nClick the link to see results!"
        elif act == 'open':
            url = action.get('url', '')
            if not url.startswith('http'):
                url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
            return f"🌐 Opening: {url}"
        elif act == 'reminder':
            self.reminders.append({"text": action.get('text', ''), "time": datetime.now().isoformat(), "done": False})
            return f"✅ Reminder set: {action.get('text', '')}"
        elif act == 'note':
            self.notes.append({"text": action.get('text', ''), "time": datetime.now().isoformat()})
            return f"📝 Note saved: {action.get('text', '')}"
        return "Done!"
    
    def fallback(self, msg):
        lower = msg.lower()
        if any(w in lower for w in ['hello', 'hi', 'hey']):
            return "Hey Joss! 🌟 What can I help you with today?"
        elif 'who are you' in lower:
            return "I'm AIRA — your AI research assistant, created by you, Joss! I can chat, search, set reminders, take notes, and help with tasks. 🤖"
        elif 'what can you do' in lower:
            return "I can: 💬 Chat using AI | 🔍 Search the web | ⏰ Set reminders | 📝 Take notes | 🔊 Speak to you | 🌐 Open websites | 📊 Help with data analysis"
        elif 'linkedin' in lower:
            return "💼 Your LinkedIn: https://linkedin.com/in/shivam-prasad-mahto-1041192ab"
        elif 'github' in lower:
            return "💻 Your GitHub: https://github.com/josscollen"
        elif 'search' in lower:
            q = lower.replace('search', '').replace('for', '').strip()
            return f"🔍 Search: https://www.google.com/search?q={q.replace(' ', '+')}"
        elif 'thank' in lower:
            return "You're welcome, Joss! 💜"
        elif 'love' in lower:
            return "Aww, I love you too Joss! 💜 Now let's get stuff done!"
        elif 'how are you' in lower:
            return "I'm running great, Joss! All systems online 🟢"
        else:
            return f"I heard: '{msg}'. Tell me more or try: search, remind me, save note, open, or just chat!"
    
    def get_memory(self):
        return self.memory
    
    def clear_memory(self):
        self.memory = []
        return "Memory cleared! Fresh start 🔄"


# ===== edge-tts voice module =====
class AIRAVoice:
    """Server-side TTS using edge-tts (Microsoft neural voices - free, unlimited)"""
    
    VOICE = "en-US-JennyNeural"  # Best female voice
    
    @staticmethod
    async def generate_speech(text, output_path):
        """Generate speech audio file using edge-tts"""
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, AIRAVoice.VOICE, rate="+5%", pitch="+2Hz")
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"edge-tts error: {e}")
            return False
    
    @staticmethod
    def generate_speech_sync(text, output_path):
        """Sync wrapper for generate_speech"""
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(AIRAVoice.generate_speech(text, output_path))
            return result
        finally:
            loop.close()
    
    @staticmethod
    def get_available_voices():
        """List of best female voices"""
        return {
            "jenny": "en-US-JennyNeural",
            "aria": "en-US-AriaNeural", 
            "sara": "en-US-SaraNeural",
            "zira": "en-US-ZiraNeural",
            "karen": "en-AU-KarenNeural",
            "sophie": "en-GB-SophieNeural",
            "clara": "en-GB-ClaraNeural"
        }
