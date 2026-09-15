# AIRA - Main Application (Render Version)
# Artificial Intelligence Research Assistant

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import hashlib

# Get the directory where this script is located
AIRA_DIR = os.path.dirname(os.path.abspath(__file__))

# Add modules to path
sys.path.insert(0, os.path.join(AIRA_DIR, 'brain'))
sys.path.insert(0, os.path.join(AIRA_DIR, 'voice'))
sys.path.insert(0, os.path.join(AIRA_DIR, 'automations'))

from aira_brain import AIRABrain
from aira_auto import AIRAAutomations

app = Flask(__name__, 
            template_folder=os.path.join(AIRA_DIR, 'ui', 'templates'),
            static_folder=os.path.join(AIRA_DIR, 'ui', 'static'))

# Password protection - only you know this
AIRA_PASSWORD = os.environ.get('AIRA_PASSWORD', 'joss2004')

# Initialize AIRA components
brain = AIRABrain()
automations = AIRAAutomations()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    """Check password"""
    data = request.json
    password = data.get('password', '')
    if password == AIRA_PASSWORD:
        return jsonify({'status': 'authenticated'})
    return jsonify({'status': 'failed', 'message': 'Wrong password'}), 401

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    password = data.get('password', '')
    
    # Check password
    if password != AIRA_PASSWORD:
        return jsonify({'response': 'Access denied. Wrong password.', 'status': 'unauthorized'}), 401
    
    response = brain.think(user_message)
    command_result = process_command(user_message)
    return jsonify({
        'response': response,
        'command': command_result,
        'status': 'success'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'name': 'AIRA',
        'version': '1.0.0',
        'status': 'online',
        'creator': 'Joss Collen',
        'brain': 'Hermes + OmniRoute',
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
    elif 'screenshot' in msg:
        return automations.take_screenshot()
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("  AIRA - Password Protected")
    print("  Only authorized users can access")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
