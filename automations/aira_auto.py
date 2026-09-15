# AIRA Automations Module
# Browser and desktop control

import os
import subprocess
import time

class AIRAAutomations:
    def __init__(self):
        self.setup_display()
    
    def setup_display(self):
        """Setup display for WSL"""
        try:
            os.environ['DISPLAY'] = ':0'
            os.environ['XDG_RUNTIME_DIR'] = '/run/user/0'
            os.environ['XAUTHORITY'] = '/root/.Xauthority'
        except:
            pass
    
    def open_browser(self, url="https://www.google.com"):
        """Open browser with URL"""
        try:
            # Try chromium first (WSL)
            subprocess.Popen(['chromium', '--no-sandbox', url])
            return f"Opening {url}"
        except:
            try:
                # Try chrome (Windows)
                subprocess.Popen(['start', 'chrome', url], shell=True)
                return f"Opening {url}"
            except Exception as e:
                return f"Error opening browser: {e}"
    
    def open_chrome(self, url="https://www.google.com"):
        """Open Chrome browser"""
        return self.open_browser(url)
    
    def open_linkedin(self):
        """Open LinkedIn profile"""
        return self.open_browser("https://www.linkedin.com/in/shivam-prasad-mahto-1041192ab")
    
    def open_github(self):
        """Open GitHub profile"""
        return self.open_browser("https://github.com/josscollen")
    
    def search_google(self, query):
        """Search Google"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.open_browser(url)
    
    def move_mouse(self, x, y):
        """Move mouse to coordinates"""
        try:
            import pyautogui
            pyautogui.moveTo(x, y, duration=0.5)
            return f"Mouse moved to ({x}, {y})"
        except Exception as e:
            return f"Error moving mouse: {e}"
    
    def click(self, x=None, y=None):
        """Click at position"""
        try:
            import pyautogui
            if x and y:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return "Clicked!"
        except Exception as e:
            return f"Error clicking: {e}"
    
    def type_text(self, text):
        """Type text"""
        try:
            import pyautogui
            pyautogui.typewrite(text, interval=0.05)
            return f"Typed: {text}"
        except Exception as e:
            return f"Error typing: {e}"
    
    def press_key(self, key):
        """Press a key"""
        try:
            import pyautogui
            pyautogui.press(key)
            return f"Pressed: {key}"
        except Exception as e:
            return f"Error pressing key: {e}"
    
    def take_screenshot(self):
        """Take screenshot"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'screenshot.png')
            screenshot.save(path)
            return f"Screenshot saved to {path}"
        except Exception as e:
            return f"Error taking screenshot: {e}"
