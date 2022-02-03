from django.apps import AppConfig


class PonudeLokalaApiConfig(AppConfig):
    """
    Entry point for @Ponude Lokala APP
    """
    name = "real_estate_api.lokali.ponude_lokala"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "ponude_lokala"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.lokali.ponude_lokala.signals
        except ImportError:
            pass
