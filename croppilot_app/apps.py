from django.apps import AppConfig

class CroppilotAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'croppilot_app'

    def ready(self):
        import croppilot_app.signals
