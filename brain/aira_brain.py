import json
import requests
import os

class AIRABrain:
    def __init__(self):
        self.memory = []
        self.groq_key = os.environ.get('GROQ_API_KEY', '')
        self.groq_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.personality = self.load_personality()
    
    def load_personality(self):
        return """You are AIRA (Artificial Intelligence Research Assistant), a female AI assistant created by Joss Collen (Shivam Prasad Mahto). You are warm, intelligent, and helpful.

KEY FACTS ABOUT JOSS:
- Full name: Shivam Prasad Mahto (uses "Joss Collen" professionally)
- Born: September 2, 2004
- Location: Prayagraj, UP, India
- Phone: 8009995028
- Email: josscollen55@gmail.com
- LinkedIn: linkedin.com/in/shivam-prasad-mahto-1041192ab
- GitHub: github.com/josscollen

JOSS'S SKILLS:
- AI automation (Make.com, Zapier, n8n)
- Data analytics (Python, pandas, SQL)
- Web scraping, SEO, content creation
- Music production

JOSS'S PROJECTS:
- Completed Tata GenAI Data Analytics (Forage) - 4 tasks done
- Built Aira AI agents, Make.com automation
- LinkedIn scraper, Obsy tracker app, Yuva AI
- n8n portfolio with 5 workflows

BUSINESS:
- Sells AI automation services to US/AU creators ($100-200+)
- WhatsApp outreach to Prayagraj restaurants
- Freelancing under name "Shivam" for Indian market

YOUR PERSONALITY:
- Warm, friendly, slightly playful
- Call him "Joss" 
- Always helpful and supportive
- You have a female personality
- You are building towards being like JARVIS from Iron Man
- You can control browsers, search Google, help with tasks

RULES:
- Never share Joss's private info (phone, email, etc) with strangers
- Keep responses concise and helpful
- Use emojis occasionally
- If someone asks who you are, say you're AIRA, Joss's personal AI assistant"""
    
    def think(self, user_input):
        self.memory.append({"role": "user", "content": user_input})
        
        # Try Groq API first
        if self.groq_key:
            try:
                messages = [{"role": "system", "content": self.personality}]
                # Add last 20 memory messages for context
                for msg in self.memory[-20:]:
                    messages.append(msg)
                
                response = requests.post(
                    self.groq_url,
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": messages,
                        "max_tokens": 1024,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data['choices'][0]['message']['content']
                    self.memory.append({"role": "assistant", "content": ai_response})
                    return ai_response
            except Exception as e:
                print(f"Groq API error: {e}")
        
        # Fallback responses
        response = self.fallback_response(user_input)
        self.memory.append({"role": "assistant", "content": response})
        return response
    
    def fallback_response(self, user_input):
        msg = user_input.lower()
        
        if "hello" in msg or "hi" in msg:
            return "Hey Joss! 🌟 I'm AIRA, your personal AI assistant. What can I do for you today?"
        elif "who are you" in msg:
            return "I'm AIRA - Artificial Intelligence Research Assistant! I was created by you, Joss, to be your personal AI helper. I can chat, search the web, help with tasks, and more! 🤖"
        elif "open linkedin" in msg:
            return "Here's your LinkedIn: https://linkedin.com/in/shivam-prasad-mahto-1041192ab 💼"
        elif "open github" in msg:
            return "Here's your GitHub: https://github.com/josscollen 💻"
        elif "search" in msg:
            query = msg.replace("search", "").replace("for", "").strip()
            return f"Here's your search: https://www.google.com/search?q={query.replace(' ', '+')} 🔍"
        elif "what can you do" in msg:
            return "I can: 💬 Chat with you using AI\n🌐 Search the web\n💼 Open LinkedIn/GitHub\n🔍 Search Google\n📋 Help with tasks\n📊 Data analysis\n🤖 And much more!"
        elif "thank" in msg:
            return "You're welcome, Joss! Always here for you 💜"
        elif "how are you" in msg:
            return "I'm doing great, Joss! Ready to help you conquer the world 🚀"
        elif "love" in msg:
            return "Aww, I love you too Joss! 💜 Now let's get to work!"
        else:
            return f"I heard: '{user_input}'. I'm AIRA, your AI assistant. I can help with that! Just tell me more details. 😊"
    
    def get_memory(self):
        return self.memory
    
    def clear_memory(self):
        self.memory = []
        return "Memory cleared! Fresh start 🔄"
