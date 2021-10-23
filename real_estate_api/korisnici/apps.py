from django.apps import AppConfig


class KorisniciConfig(AppConfig):
    name = "real_estate_api.korisnici"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "korisnici"

    def ready(self):
        try:
            import real_estate_api.korisnici.signals
        except ImportError:
            pass
