import json
import aiofiles
from datetime import datetime, timedelta
from pathlib import Path

class NotificationManager:
    def __init__(self, history_file="data/notification_history.json", throttle_minutes=30):
        self.history_file = Path(history_file)
        self.throttle_minutes = throttle_minutes
        self.sent_notifications = {}  # In-memory cache for throttling
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
    def _get_notification_key(self, flight):
        """Create a unique key for a flight notification."""
        return f"{flight.get('airline', 'Unknown')}_{flight.get('destination', 'Unknown')}_{flight.get('price', 0)}"
    
    def _load_history(self):
        """Load notification history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading notification history: {e}")
        return {"notifications": [], "throttle_cache": {}}
    
    def _save_history(self, data):
        """Save notification history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving notification history: {e}")
    
    def is_throttled(self, flight):
        """Check if notification for this flight should be throttled."""
        key = self._get_notification_key(flight)
        now = datetime.now()
        
        # Check in-memory cache first
        if key in self.sent_notifications:
            last_sent = self.sent_notifications[key]
            if now - last_sent < timedelta(minutes=self.throttle_minutes):
                return True
        
        # Check file-based history
        history = self._load_history()
        throttle_cache = history.get("throttle_cache", {})
        
        if key in throttle_cache:
            last_sent_str = throttle_cache[key]
            try:
                last_sent = datetime.fromisoformat(last_sent_str)
                if now - last_sent < timedelta(minutes=self.throttle_minutes):
                    return True
            except:
                pass
        
        return False
    
    def record_notification(self, flight, channels_used):
        """Record that a notification was sent."""
        key = self._get_notification_key(flight)
        now = datetime.now()
        
        # Update in-memory cache
        self.sent_notifications[key] = now
        
        # Update file-based history
        history = self._load_history()
        
        # Add to notification history
        notification_record = {
            "timestamp": now.isoformat(),
            "airline": flight.get("airline", "Unknown"),
            "destination": flight.get("destination", "Unknown"),
            "price": flight.get("price", 0),
            "channels": channels_used
        }
        history["notifications"].append(notification_record)
        
        # Update throttle cache
        history["throttle_cache"][key] = now.isoformat()
        
        # Keep only last 100 notifications to prevent file bloat
        if len(history["notifications"]) > 100:
            history["notifications"] = history["notifications"][-100:]
        
        # Clean old throttle entries (older than 24 hours)
        cutoff_time = now - timedelta(hours=24)
        history["throttle_cache"] = {
            k: v for k, v in history["throttle_cache"].items()
            if datetime.fromisoformat(v) > cutoff_time
        }
        
        self._save_history(history)
    
    def get_recent_notifications(self, hours=24):
        """Get notifications from the last N hours."""
        history = self._load_history()
        notifications = history.get("notifications", [])
        
        if not notifications:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent = []
        
        for notification in notifications:
            try:
                timestamp = datetime.fromisoformat(notification["timestamp"])
                if timestamp > cutoff_time:
                    recent.append(notification)
            except:
                continue
        
        return recent
    
    def get_notification_stats(self):
        """Get statistics about notifications."""
        history = self._load_history()
        notifications = history.get("notifications", [])
        
        if not notifications:
            return {"total": 0, "today": 0, "this_week": 0}
        
        now = datetime.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        
        today_count = 0
        week_count = 0
        
        for notification in notifications:
            try:
                timestamp = datetime.fromisoformat(notification["timestamp"])
                if timestamp.date() == today:
                    today_count += 1
                if timestamp > week_ago:
                    week_count += 1
            except:
                continue
        
        return {
            "total": len(notifications),
            "today": today_count,
            "this_week": week_count
        } 