from django.apps import AppConfig


class KorisniciConfig(AppConfig):
    """
    Entry point form @Korisnici APP
    """
    name = "real_estate_api.korisnici"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "korisnici"

    def ready(self):
        """If we are needed from some signals post or pre save"""
        try:
            import real_estate_api.korisnici.signals
        except ImportError:
            pass
