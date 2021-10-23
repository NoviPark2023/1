from django.apps import AppConfig


class KupciConfig(AppConfig):
    name = "real_estate_api.kupci"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "kupci"

    def ready(self):
        try:
            import real_estate_api.kupci.signals
        except ImportError:
            pass