from django.apps import AppConfig


class KupciConfig(AppConfig):
    """
    Entry point form @Kupci APP
    """
    name = "real_estate_api.kupci"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "kupci"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.kupci.signals
        except ImportError:
            pass
