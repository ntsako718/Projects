# Generated by Django 5.1.6 on 2025-03-27 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Topwinz_app', '0003_raffle_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffle',
            name='countdown_seconds',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='raffle',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
