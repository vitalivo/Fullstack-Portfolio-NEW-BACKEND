from django.apps import AppConfig

class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
    verbose_name = 'Контакты'

    def ready(self):
        import apps.contacts.signals # Импортируем сигналы, чтобы они были зарегистрированы
