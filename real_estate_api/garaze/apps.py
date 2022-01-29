from django.apps import AppConfig


class GarazeConfig(AppConfig):
    """
    Entry point for @Garaze APP.
    """
    name = "real_estate_api.garaze"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "garaze"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.garaze.signals
        except ImportError:
            pass
