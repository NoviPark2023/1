from django.apps import AppConfig


class PonudeConfig(AppConfig):
    """
    Entry point form @Ponude APP
    """
    name = "real_estate_api.ponude"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "ponude"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.ponude.signals
        except ImportError:
            pass