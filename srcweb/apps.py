from django.apps import AppConfig


class SrcwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'srcweb'

    def ready(self):
        import srcweb.signals  # This will register the signals