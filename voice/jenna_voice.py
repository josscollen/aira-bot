# JENNA - Voice Engine
# Independent voice - no Microsoft, no browser dependency

import os
import tempfile
import asyncio

class JENNAVoice:
    """Jenna's own voice engine using OpenVox + Groq Whisper"""
    
    @staticmethod
    async def generate_speech(text, output_path=None):
        """Generate speech using OpenVox TTS (fully offline, independent)"""
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), 'jenna_speech.wav')
        
        try:
            from openvox.tts import TTSEngine
            engine = TTSEngine()
            audio = engine.synthesize(text)
            engine.save(audio, output_path)
            return output_path
        except ImportError:
            # Fallback: use edge-tts with Ava voice (best female)
            import edge_tts
            c = edge_tts.Communicate(text, "en-US-AvaNeural", rate="+3%", pitch="+1Hz")
            mp3_path = output_path.replace('.wav', '.mp3')
            await c.save(mp3_path)
            return mp3_path
        except Exception as e:
            print(f"OpenVox error: {e}, falling back to edge-tts")
            import edge_tts
            c = edge_tts.Communicate(text, "en-US-AvaNeural", rate="+3%", pitch="+1Hz")
            mp3_path = output_path.replace('.wav', '.mp3')
            await c.save(mp3_path)
            return mp3_path
    
    @staticmethod
    async def generate_speech_clone(text, reference_audio, output_path=None):
        """Generate speech using cloned voice"""
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), 'jenna_cloned.wav')
        
        try:
            from openvox.clone import VoiceCloner
            cloner = VoiceCloner()
            voice = cloner.enroll(reference_audio)
            audio = cloner.synthesize(text, voice=voice)
            cloner.save(audio, output_path)
            return output_path
        except Exception as e:
            print(f"Clone error: {e}")
            return None
    
    @staticmethod
    def transcribe_audio(audio_file_path, api_key=None):
        """Transcribe audio using Groq Whisper (server-side, no browser mic)"""
        import requests
        
        if not api_key:
            api_key = os.environ.get('GROQ_API_KEY', '')
        
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        
        with open(audio_file_path, 'rb') as f:
            files = {'file': (os.path.basename(audio_file_path), f, 'audio/wav')}
            data = {
                'model': 'whisper-large-v3-turbo',
                'response_format': 'json'
            }
            headers = {'Authorization': f'Bearer {api_key}'}
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('text', '')
            else:
                return f"STT error: {response.status_code}"

# Sync wrapper
def speak(text):
    voice = JENNAVoice()
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(voice.generate_speech(text))
    finally:
        loop.close()

def listen(audio_path):
    return JENNAVoice.transcribe_audio(audio_path)
