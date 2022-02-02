from django.apps import AppConfig


class LokaliApiConfig(AppConfig):
    """
    Entry point form @Lokali APP
    """
    name = "real_estate_api.lokali.lokali_api"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "lokali_api"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.lokali.lokali_api.signals
        except ImportError:
            pass
