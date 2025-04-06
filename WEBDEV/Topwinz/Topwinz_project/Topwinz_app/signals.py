from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RaffleEntry, Raffle

@receiver(post_save, sender=RaffleEntry)
def check_raffle_status(sender, instance, **kwargs):
    """
    Checks if all tickets are sold and triggers the countdown.
    """
    raffle = instance.raffle
    if raffle.tickets_left == 0 and raffle.is_active:
        # Mark the raffle as started
        raffle.started = True
        raffle.save()

        # You can emit an event here (WebSocket, API, or JavaScript fetch)
        print(f"🎉 Raffle {raffle.id} is sold out! Countdown starting... 🚀")
