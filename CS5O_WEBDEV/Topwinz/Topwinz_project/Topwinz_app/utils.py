from django.utils import timezone
import datetime

def calculate_time_left(raffle):
    """Calculate remaining time in seconds for the raffle countdown"""
    if not raffle.started or not raffle.start_time:
        return 0
    
    elapsed = timezone.now() - raffle.start_time
    remaining = max(0, raffle.countdown_seconds - elapsed.total_seconds())
    return int(remaining)