# AIRA Configuration
# Default settings

import os

AIRA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CONFIG = {
    "name": "AIRA",
    "full_name": "Artificial Intelligence Research Assistant",
    "version": "1.0.0",
    "creator": "Joss Collen",
    "voice": {
        "engine": "pyttsx3",
        "gender": "female",
        "voice_id": "english_rp_female",
        "rate": 150,
        "volume": 1.0
    },
    "brain": {
        "provider": "omniroute",
        "fallback": "backup_api",
        "model": "default"
    },
    "safety": {
        "confirm_dangerous": True,
        "allowed_folders": ["D:/AIRA", "D:/Documents", "C:/Users/DELL"],
        "blocked_folders": ["C:/Windows", "C:/Program Files"],
        "log_all_actions": True
    },
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": False
    }
}

def load_config():
    """Load configuration"""
    import json
    config_path = os.path.join(AIRA_DIR, 'config', 'aira_config.json')
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        # Create default config
        with open(config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration"""
    import json
    config_path = os.path.join(AIRA_DIR, 'config', 'aira_config.json')
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return True
