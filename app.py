# AIRA - Main Application (Render Version)
from flask import Flask, render_template, request, jsonify, send_file
import os, sys, tempfile

AIRA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AIRA_DIR, 'brain'))

from aira_brain import AIRABrain, AIRAVoice

app = Flask(__name__, 
            template_folder=os.path.join(AIRA_DIR, 'ui', 'templates'),
            static_folder=os.path.join(AIRA_DIR, 'ui', 'static'))

AIRA_PASSWORD = 'Jossloveaira@123'
brain = AIRABrain()

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
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@app.route('/api/speak', methods=['POST'])
def speak():
    """Generate speech audio using edge-tts"""
    data = request.json
    if data.get('password', '') != AIRA_PASSWORD:
        return jsonify({'status': 'unauthorized'}), 401
    
    text = data.get('text', '')
    if not text:
        return jsonify({'status': 'no text'}), 400
    
    # Generate audio
    output = os.path.join(tempfile.gettempdir(), 'aira_speech.mp3')
    success = AIRAVoice.generate_speech_sync(text, output)
    
    if success and os.path.exists(output):
        return send_file(output, mimetype='audio/mpeg', as_attachment=False)
    
    return jsonify({'status': 'tts error'}), 500

@app.route('/api/voices')
def voices():
    return jsonify(AIRAVoice.get_available_voices())

@app.route('/api/status')
def status():
    return jsonify({
        'name': 'AIRA', 'version': '3.0.0', 'status': 'online',
        'creator': 'Joss Collen', 'brain': 'Groq AI + edge-tts',
        'protected': True
    })

@app.route('/api/memory')
def memory():
    return jsonify({'memory': brain.get_memory()})

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    brain.clear_memory()
    return jsonify({'status': 'memory cleared'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
