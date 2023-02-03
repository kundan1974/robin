from django.apps import AppConfig


class PatientDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patient_data'

    def ready(self):
        import patient_data.signals