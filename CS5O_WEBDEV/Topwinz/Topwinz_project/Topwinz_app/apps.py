from django.apps import AppConfig


class TopwinzAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Topwinz_app'

class RaffleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Topwinz_app'

    def ready(self):
        import Topwinz_app.signals  # Ensures signals are registered