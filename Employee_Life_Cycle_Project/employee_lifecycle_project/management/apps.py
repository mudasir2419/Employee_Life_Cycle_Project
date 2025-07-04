
from django.apps import AppConfig
from .queue_worker import start_worker

class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'

    def ready(self):
        start_worker()

