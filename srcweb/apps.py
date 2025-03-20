from django.apps import AppConfig


class SrcwebConfig(AppConfig):
    # Specifies the default field type for auto generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'srcweb'

    def ready(self):
        # Imports signals module, registering signal handlers when the app loads
        import srcweb.signals