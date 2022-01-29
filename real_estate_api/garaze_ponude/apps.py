from django.apps import AppConfig


class GarazePonudeConfig(AppConfig):
    """
    Entry point for @Ponude Garaze APP.
    """

    name = "real_estate_api.garaze_ponude"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "garaze_ponude"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.garaze_ponude.signals
        except ImportError:
            pass


