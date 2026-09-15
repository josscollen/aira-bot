# AIRA Voice Module
# Female voice for AIRA

import os

def get_voice_config():
    """Get voice configuration for AIRA"""
    return {
        "engine": "pyttsx3",
        "gender": "female",
        "voice_name": "English (Great Britain)",
        "rate": 150,
        "volume": 1.0
    }

def speak(text, save_only=False):
    """Speak text using female voice"""
    import pyttsx3
    
    # Try to setup display (WSL)
    try:
        os.environ['DISPLAY'] = ':0'
        os.environ['XDG_RUNTIME_DIR'] = '/run/user/0'
        os.environ['XAUTHORITY'] = '/root/.Xauthority'
    except:
        pass
    
    engine = pyttsx3.init()
    
    # Get voices and find female
    voices = engine.getProperty('voices')
    for voice in voices:
        # Prefer British female voice
        if 'Great Britain' in voice.name or 'Received Pronunciation' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    
    # Set rate and volume
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    if save_only:
        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), 'aira_speech.wav')
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return output_path
    else:
        # Speak directly
        engine.say(text)
        engine.runAndWait()
        return None

def speak_and_save(text):
    """Speak and save to file for phone access"""
    import pyttsx3
    
    # Try to setup display (WSL)
    try:
        os.environ['DISPLAY'] = ':0'
        os.environ['XDG_RUNTIME_DIR'] = '/run/user/0'
        os.environ['XAUTHORITY'] = '/root/.Xauthority'
    except:
        pass
    
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'Great Britain' in voice.name or 'Received Pronunciation' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), 'aira_speech.wav')
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    # Also play it
    engine.say(text)
    engine.runAndWait()
    
    return output_path
