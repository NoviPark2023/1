from django.apps import AppConfig


class LokaliDmsConfig(AppConfig):
    """
    Entry point for @LokaliDmsConfig APP.
    """
    name = "real_estate_api.lokali.lokali_dms"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "lokali_dms"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.lokali.lokali_dms.signals
        except ImportError:
            pass
