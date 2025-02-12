from datetime import timedelta, timezone, datetime
from .models import HotTopic

def is_last_hottopic_old(hotTopic):
    if hotTopic:
        # Get the current time in UTC
        now = datetime.now(timezone.utc)

        # Check if the last entry is older than 4 hours
        if now - hotTopic.created_at > timedelta(hours=4):
            return True  # More than 4 hours old
        else:
            return False  # Still fresh
    else:
        return True  # No entries exist, so it's "old" by default