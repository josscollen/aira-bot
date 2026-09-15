# AIRA - Main Application
# Artificial Intelligence Research Assistant

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import json
import threading
import time

# Get the directory where this script is located
AIRA_DIR = os.path.dirname(os.path.abspath(__file__))

# Add modules to path
sys.path.insert(0, os.path.join(AIRA_DIR, 'brain'))
sys.path.insert(0, os.path.join(AIRA_DIR, 'voice'))
sys.path.insert(0, os.path.join(AIRA_DIR, 'automations'))

from aira_brain import AIRABrain
from aira_voice import speak, speak_and_save
from aira_auto import AIRAAutomations

app = Flask(__name__, 
            template_folder=os.path.join(AIRA_DIR, 'ui', 'templates'),
            static_folder=os.path.join(AIRA_DIR, 'ui', 'static'))

# Initialize AIRA components
brain = AIRABrain()
automations = AIRAAutomations()

@app.route('/')
def home():
    """Main AIRA interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message"""
    data = request.json
    user_message = data.get('message', '')
    
    # Get AI response
    response = brain.think(user_message)
    
    # Process commands
    command_result = process_command(user_message)
    
    return jsonify({
        'response': response,
        'command': command_result,
        'status': 'success'
    })

@app.route('/api/voice', methods=['POST'])
def voice():
    """Process voice input"""
    data = request.json
    text = data.get('text', '')
    
    # Get AI response
    response = brain.think(text)
    
    # Generate speech file
    voice_path = speak_and_save(response)
    
    return jsonify({
        'response': response,
        'voice_file': '/api/voice-file',
        'status': 'success'
    })

@app.route('/api/voice-file')
def voice_file():
    """Serve voice file"""
    voice_path = os.path.join(AIRA_DIR, 'voice', 'aira_speech.wav')
    if os.path.exists(voice_path):
        return send_file(voice_path, mimetype='audio/wav')
    return jsonify({'error': 'No voice file'}), 404

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Speak text directly"""
    data = request.json
    text = data.get('text', '')
    speak(text)
    return jsonify({'status': 'speaking'})

@app.route('/api/command', methods=['POST'])
def command():
    """Execute automation command"""
    data = request.json
    command = data.get('command', '')
    result = execute_command(command)
    return jsonify({'result': result, 'status': 'success'})

@app.route('/api/status')
def status():
    """Get AIRA status"""
    return jsonify({
        'name': 'AIRA',
        'version': '1.0.0',
        'status': 'online',
        'creator': 'Joss Collen',
        'voice': 'female',
        'brain': 'Hermes + OmniRoute'
    })

@app.route('/api/memory')
def memory():
    """Get conversation memory"""
    return jsonify({'memory': brain.get_memory()})

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    """Clear conversation memory"""
    brain.clear_memory()
    return jsonify({'status': 'memory cleared'})

def process_command(message):
    """Process user commands"""
    msg = message.lower()
    
    if 'open linkedin' in msg:
        return automations.open_linkedin()
    elif 'open github' in msg:
        return automations.open_github()
    elif 'open chrome' in msg or 'open browser' in msg:
        return automations.open_browser()
    elif 'search' in msg:
        query = msg.replace('search', '').replace('for', '').strip()
        return automations.search_google(query)
    elif 'screenshot' in msg:
        return automations.take_screenshot()
    elif 'click' in msg:
        return automations.click()
    elif 'type' in msg:
        text = msg.replace('type', '').strip()
        return automations.type_text(text)
    
    return None

def execute_command(command):
    """Execute automation command"""
    try:
        cmd_parts = command.split()
        if cmd_parts[0] == 'open':
            if len(cmd_parts) > 1:
                return automations.open_browser(cmd_parts[1])
        elif cmd_parts[0] == 'move':
            if len(cmd_parts) == 3:
                return automations.move_mouse(int(cmd_parts[1]), int(cmd_parts[2]))
        elif cmd_parts[0] == 'click':
            if len(cmd_parts) == 3:
                return automations.click(int(cmd_parts[1]), int(cmd_parts[2]))
        elif cmd_parts[0] == 'type':
            return automations.type_text(' '.join(cmd_parts[1:]))
        elif cmd_parts[0] == 'key':
            return automations.press_key(cmd_parts[1])
        elif cmd_parts[0] == 'screenshot':
            return automations.take_screenshot()
        
        return "Unknown command"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    print("=" * 50)
    print("  AIRA - Artificial Intelligence Research Assistant")
    print("  Created by Joss Collen")
    print("  Voice: Female (British)")
    print("  Brain: Hermes + OmniRoute")
    print("=" * 50)
    print()
    print("Starting AIRA server...")
    print("Open http://localhost:5000 in your browser")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
