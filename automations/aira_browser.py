# AIRA Browser Control Module
# Uses browser-use for AI-powered browser automation

import os
import asyncio
import json

class AIRABrowser:
    """Browser automation for AIRA using browser-use"""
    
    def __init__(self):
        self.status = "ready"
    
    async def browse(self, task, api_key=None):
        """Use browser-use AI agent to perform a browser task"""
        try:
            from browser_use import Agent
            from langchain_openai import ChatOpenAI
            
            # Use Groq or OpenAI-compatible API
            if api_key:
                llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
            else:
                # Use browser-use's built-in or user's key
                llm = ChatOpenAI(model="gpt-4o-mini")
            
            agent = Agent(
                task=task,
                llm=llm
            )
            result = await agent.run()
            return result.final_result()
        except Exception as e:
            return f"Browser error: {str(e)}"
    
    def search_web(self, query):
        """Simple web search"""
        return f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    def open_site(self, url):
        """Open a website"""
        if not url.startswith('http'):
            url = f"https://{url}"
        return url
    
    def get_status(self):
        return {"browser": self.status, "capabilities": ["search", "browse", "fill forms", "navigate"]}

# Simple sync wrapper
def browser_task(task):
    browser = AIRABrowser()
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(browser.browse(task))
    finally:
        loop.close()
