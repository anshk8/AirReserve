#!/usr/bin/env python3
"""
Debug script to check configuration loading
"""

import json
from pathlib import Path

def debug_config():
    """Debug the configuration loading"""
    
    # Load config directly
    config_file = Path("config/notification_config.json")
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("📋 Configuration loaded:")
        print(f"   Threshold: ${config.get('threshold', 'NOT SET')}")
        print(f"   Channels: {config.get('notification_channels', 'NOT SET')}")
        print(f"   Discord Webhook: {'SET' if config.get('discord_webhook_url') else 'NOT SET'}")
        
        if config.get('discord_webhook_url'):
            webhook = config['discord_webhook_url']
            print(f"   Webhook URL: {webhook[:50]}...")
        else:
            print("   ❌ No Discord webhook URL found!")
            
    else:
        print(f"❌ Config file not found: {config_file}")
    
    # Check if discord is in channels
    channels = config.get('notification_channels', [])
    if 'discord' in channels:
        print("   ✅ Discord is in notification channels")
    else:
        print("   ❌ Discord is NOT in notification channels")

if __name__ == "__main__":
    debug_config() 