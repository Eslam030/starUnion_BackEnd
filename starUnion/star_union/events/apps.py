from django.apps import AppConfig
import time


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self) -> None:
        import events.signals
        import events.serializer
        import events.tasks
        from events.tasks import background_task
        # background_task()
