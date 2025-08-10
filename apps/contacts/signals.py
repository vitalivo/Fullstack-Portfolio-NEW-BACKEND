from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContactMessage
from .utils import send_contact_notification # Импортируем нашу функцию

@receiver(post_save, sender=ContactMessage)
def contact_message_post_save(sender, instance, created, **kwargs):
    """
    Сигнал, который отправляет уведомления после сохранения нового ContactMessage.
    """
    if created: # Отправляем уведомление только при создании нового сообщения
        send_contact_notification(instance)
        # Автоматически помечаем как прочитанное после отправки уведомлений
        instance.mark_as_read()
