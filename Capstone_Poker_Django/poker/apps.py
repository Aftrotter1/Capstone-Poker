from django.apps import AppConfig


class PokerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poker'
        # add this
    def ready(self):
        import poker.signals  # noqa