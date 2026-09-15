# AIRA - Main Application (Render Version)
# Artificial Intelligence Research Assistant

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys

AIRA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AIRA_DIR, 'brain'))
sys.path.insert(0, os.path.join(AIRA_DIR, 'automations'))

from aira_brain import AIRABrain
from aira_auto import AIRAAutomations

app = Flask(__name__, 
            template_folder=os.path.join(AIRA_DIR, 'ui', 'templates'),
            static_folder=os.path.join(AIRA_DIR, 'ui', 'static'))

AIRA_PASSWORD = 'Jossloveaira@123'
brain = AIRABrain()
automations = AIRAAutomations()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.json
    if data.get('password', '') == AIRA_PASSWORD:
        return jsonify({'status': 'authenticated'})
    return jsonify({'status': 'failed'}), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if data.get('password', '') != AIRA_PASSWORD:
        return jsonify({'response': 'Access denied.', 'status': 'unauthorized'}), 401
    
    user_message = data.get('message', '')
    response = brain.think(user_message)
    command_result = process_command(user_message)
    
    return jsonify({
        'response': response,
        'command': command_result,
        'status': 'success'
    })

@app.route('/api/voice-speak', methods=['POST'])
def voice_speak():
    """Return text for browser TTS"""
    data = request.json
    if data.get('password', '') != AIRA_PASSWORD:
        return jsonify({'status': 'unauthorized'}), 401
    return jsonify({'text': data.get('text', ''), 'status': 'success'})

@app.route('/api/status')
def status():
    return jsonify({
        'name': 'AIRA',
        'version': '2.0.0',
        'status': 'online',
        'creator': 'Joss Collen',
        'brain': 'Groq AI',
        'protected': True
    })

@app.route('/api/memory')
def memory():
    return jsonify({'memory': brain.get_memory()})

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    brain.clear_memory()
    return jsonify({'status': 'memory cleared'})

def process_command(message):
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
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
