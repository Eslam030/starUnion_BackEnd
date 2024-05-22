from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workshops'

    def ready(self) -> None:
        import workshops.signals
        import workshops.serializer
