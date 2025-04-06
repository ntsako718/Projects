from django.contrib import admin
from .models import Raffle, RaffleEntry

# Register your models here.
admin.site.register(Raffle)
admin.site.register(RaffleEntry)
