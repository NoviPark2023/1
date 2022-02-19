from django.apps import AppConfig


class StanoviDmsConfig(AppConfig):
    """
    Entry point for @StanoviDmsConfig APP.
    """
    name = "real_estate_api.stanovi.stanovi_dms"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "stanovi_dms"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.stanovi.stanovi_dms.signals
        except ImportError:
            pass

