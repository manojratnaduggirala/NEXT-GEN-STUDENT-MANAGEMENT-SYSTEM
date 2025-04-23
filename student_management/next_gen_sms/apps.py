from django.apps import AppConfig

class NextGenSmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'next_gen_sms'

    def ready(self):
        import next_gen_sms.signals  # Ensure signals are imported

        


