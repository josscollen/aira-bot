# JENNA - Main Application
# Joss's Enhanced Neural Network Assistant

from flask import Flask, render_template, request, jsonify, send_file
import os, sys, tempfile, json

AIRA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AIRA_DIR, 'brain'))

from jenna_brain import JENNABrain

app = Flask(__name__, 
            template_folder=os.path.join(AIRA_DIR, 'ui', 'templates'),
            static_folder=os.path.join(AIRA_DIR, 'ui', 'static'))

AIRA_PASSWORD = 'Jossloveaira@123'
brain = JENNABrain()

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
    return jsonify({'response': response, 'status': 'success'})

@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.json
    if data.get('password', '') != AIRA_PASSWORD:
        return jsonify({'status': 'unauthorized'}), 401
    text = data.get('text', '')
    if not text:
        return jsonify({'status': 'no text'}), 400
    
    import asyncio
    import edge_tts
    
    async def gen_speech():
        voice = "en-US-AvaNeural"
        c = edge_tts.Communicate(text, voice, rate="+3%", pitch="+1Hz")
        output = os.path.join(tempfile.gettempdir(), 'jenna_speech.mp3')
        await c.save(output)
        return output
    
    try:
        output = asyncio.run(gen_speech())
        if os.path.exists(output):
            return send_file(output, mimetype='audio/mpeg', as_attachment=False)
    except Exception as e:
        print(f"TTS error: {e}")
    
    return jsonify({'status': 'tts error'}), 500

@app.route('/api/listen', methods=['POST'])
def listen():
    """Server-side STT using Groq Whisper"""
    if request.form.get('password', '') != AIRA_PASSWORD:
        return jsonify({'text': '', 'status': 'unauthorized'}), 401
    
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'text': '', 'status': 'no audio'}), 400
    
    # Save audio to temp
    temp_path = os.path.join(tempfile.gettempdir(), 'jenna_input.webm')
    audio_file.save(temp_path)
    
    groq_key = os.environ.get('GROQ_API_KEY', '')
    if not groq_key:
        # Fallback: return empty, user can type
        return jsonify({'text': '', 'status': 'no API key - type instead'}), 200
    
    # Send to Groq Whisper API
    import requests
    try:
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        with open(temp_path, 'rb') as f:
            files = {'file': ('recording.webm', f, 'audio/webm')}
            data = {'model': 'whisper-large-v3-turbo', 'response_format': 'json'}
            headers = {'Authorization': f'Bearer {groq_key}'}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        
        if resp.status_code == 200:
            text = resp.json().get('text', '')
            return jsonify({'text': text, 'status': 'success'})
        else:
            return jsonify({'text': '', 'status': 'whisper error'}), 500
    except Exception as e:
        return jsonify({'text': '', 'status': str(e)}), 500

@app.route('/api/status')
def status():
    return jsonify({'name': 'JENNA', 'version': '1.0.0', 'status': 'online',
        'creator': 'Joss Collen', 'full_name': "Joss's Enhanced Neural Network Assistant"})

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
