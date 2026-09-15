# AIRA Skills Module
# What AIRA can do

SKILLS = {
    "browser": {
        "name": "Browser Control",
        "commands": [
            "open linkedin",
            "open github", 
            "open chrome",
            "open browser",
            "search [query]",
            "take screenshot"
        ],
        "description": "Control web browsers and navigate websites"
    },
    "desktop": {
        "name": "Desktop Control",
        "commands": [
            "move mouse [x] [y]",
            "click [x] [y]",
            "type [text]",
            "press [key]"
        ],
        "description": "Control mouse and keyboard"
    },
    "voice": {
        "name": "Voice Control",
        "commands": [
            "speak [text]",
            "listen",
            "stop listening"
        ],
        "description": "Voice input and output"
    },
    "automation": {
        "name": "Automation",
        "commands": [
            "open app [name]",
            "run script [path]",
            "schedule task"
        ],
        "description": "Automate repetitive tasks"
    },
    "information": {
        "name": "Information",
        "commands": [
            "who are you",
            "what can you do",
            "help",
            "status"
        ],
        "description": "Get information about AIRA"
    }
}

def get_skills():
    """Get all available skills"""
    return SKILLS

def get_skill(name):
    """Get specific skill"""
    return SKILLS.get(name, None)

def list_commands():
    """List all available commands"""
    commands = []
    for skill in SKILLS.values():
        commands.extend(skill["commands"])
    return commands
