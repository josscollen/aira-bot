# AIRA Log Module
# Log all actions for safety

import os
import json
from datetime import datetime

LOG_DIR = "/mnt/d/AIRA/logs"

def log_action(action, details=None):
    """Log an action"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "action": action,
        "details": details
    }
    
    # Create log file for today
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"log_{today}.json")
    
    # Append to log
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return log_entry

def get_logs(date=None):
    """Get logs for a specific date"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    log_file = os.path.join(LOG_DIR, f"log_{date}.json")
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return json.load(f)
    
    return []

def get_recent_logs(count=10):
    """Get recent logs"""
    logs = []
    for i in range(7):  # Last 7 days
        date = datetime.now().strftime("%Y-%m-%d")
        logs.extend(get_logs(date))
    
    return logs[-count:]
