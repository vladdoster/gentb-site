from django.apps import AppConfig
from django.db.models import signals


class UploadsConfig(AppConfig):
    name = 'apps.uploads'

    @staticmethod
    def remove_files(instance, **kw):
        instance.delete_now()

    def ready(self):
        from .models import UploadFile
        signals.pre_delete.connect(self.remove_files, sender=UploadFile)
