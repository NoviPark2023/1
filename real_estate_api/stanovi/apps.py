from django.apps import AppConfig


class StanoviConfig(AppConfig):
    name = "real_estate_api.stanovi"
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "stanovi"

    def ready(self):
        try:
            import real_estate_api.stanovi.signals
        except ImportError:
            pass
