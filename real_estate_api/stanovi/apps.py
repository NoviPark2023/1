from django.apps import AppConfig


class StanoviConfig(AppConfig):
    """
    Entry point form @Stanovi APP
    """
    name = "real_estate_api.stanovi"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "stanovi"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.stanovi.signals
        except ImportError:
            pass
