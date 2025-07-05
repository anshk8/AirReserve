#!/usr/bin/env python3
"""
Clear notification history to test fresh notifications
"""

import json
from pathlib import Path

def clear_history():
    """Clear notification history"""
    
    history_file = Path("data/notification_history.json")
    
    if history_file.exists():
        # Clear the history
        empty_history = {
            "notifications": [],
            "throttle_cache": {}
        }
        
        with open(history_file, 'w') as f:
            json.dump(empty_history, f, indent=2)
        
        print("🗑️  Notification history cleared!")
    else:
        print("📁 No notification history file found")

if __name__ == "__main__":
    clear_history() 