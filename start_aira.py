# AIRA - Startup Script
# Run this to start AIRA

import os
import sys
import subprocess
import time

print("=" * 60)
print()
print("     █████╗  █████╗ ███████╗██╗  ██╗██╗ ██████╗ ")
print("    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██╔════╝ ")
print("    ███████║███████║███████╗███████║██║██║  ███╗")
print("    ██╔══██║██╔══██║╚════██║██╔══██║██║██║   ██║")
print("    ██║  ██║██║  ██║███████║██║  ██║██║╚██████╔╝")
print("    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ")
print()
print("     Artificial Intelligence Research Assistant")
print("     Created by Joss Collen")
print()
print("=" * 60)
print()

# Get the directory where this script is located
aira_dir = os.path.dirname(os.path.abspath(__file__))
print(f"AIRA directory: {aira_dir}")

# Check if running from correct directory
if not os.path.exists(aira_dir):
    print("Error: AIRA directory not found!")
    print("Please make sure AIRA is installed correctly.")
    sys.exit(1)

# Check for required packages
print("\nChecking dependencies...")
required = ['flask', 'pyttsx3', 'requests']
missing = []

for package in required:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - MISSING")
        missing.append(package)

if missing:
    print(f"\nInstalling missing packages: {', '.join(missing)}")
    subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)

print("\nAll dependencies satisfied!")
print()

# Setup environment
os.environ['DISPLAY'] = ':0'
os.environ['XDG_RUNTIME_DIR'] = '/run/user/0'
os.environ['XAUTHORITY'] = '/root/.Xauthority'

# Import and run the app
sys.path.insert(0, aira_dir)
from app import app

print("Starting AIRA server...")
print()
print("  → Open http://localhost:5000 in your browser")
print("  → Or http://YOUR_IP:5000 from another device")
print()
print("  Voice: Female (British)")
print("  Brain: Hermes + OmniRoute")
print()

app.run(host='0.0.0.0', port=5000, debug=False)
