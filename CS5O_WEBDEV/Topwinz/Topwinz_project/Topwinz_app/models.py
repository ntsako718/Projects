from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone
from .utils import calculate_time_left

# Create your models here.

class Raffle(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="raffle_images/")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.IntegerField()
    is_active = models.BooleanField(default=True)
    started = models.BooleanField(default=False)  # Marks if raffle has started
    ended = models.BooleanField(default=False)  # New field for clarity
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)  # Track the time when the raffle starts
    countdown_seconds = models.IntegerField(default=10)  # Countdown duration in seconds, set to 10 for 10 seconds
    tickets_left = models.IntegerField()

    def send_winner_email(self):
        """Notifies the winner via email."""
        if self.winner:
            subject = "🎉 Congratulations! You've Won the Raffle!"
            message = f"Dear {self.winner.username},\n\nYou've won the price: {self.name}! We'll contact you for delivery details."
            self.winner.email_user(subject, message)

    def starting_time(self):
        self.started = True
        self.start_time = timezone.now()  # Set the current time as the start time
        self.save()

    def pick_winner(self):
    ### Picks a random winner when tickets sell out and countdown ends"""
        if self.tickets_left == 0 and self.started and not self.ended:
            entries = RaffleEntry.objects.filter(raffle=self)
            if entries.exists():
                # Select winner randomly
                winner_entry = random.choice(entries)
                self.winner = winner_entry.user
                self.ended = True  # Mark raffle as ended
                self.is_active = False  # Mark as inactive
                self.save()
                
                # Send email to winner
                self.send_winner_email()
                return self.winner
            else:
                print("No entries found in this raffle")
        return None
    
    

class RaffleEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)


