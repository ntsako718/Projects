# Generated by Django 5.1.6 on 2025-03-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Topwinz_app', '0004_raffle_countdown_seconds_raffle_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffle',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
