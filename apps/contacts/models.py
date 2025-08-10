from django.db import models
from django.core.validators import validate_email

class ContactMessage(models.Model):
    """Сообщения обратной связи"""
    
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('read', 'Прочитано'),
        ('replied', 'Отвечено'),
        ('archived', 'Архивировано'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('normal', 'Обычный'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    # Информация отправителя
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email', validators=[validate_email])
    phone = models.CharField('Телефон', max_length=20, blank=True)
    company = models.CharField('Компания', max_length=100, blank=True)
    
    # Сообщение
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение')
    
    # Классификация
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField('Приоритет', max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Дополнительная информация
    source = models.CharField('Источник', max_length=50, default='website', help_text='Откуда пришло сообщение')
    user_agent = models.TextField('User Agent', blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    
    # Ответ
    reply_message = models.TextField('Ответ', blank=True)
    replied_at = models.DateTimeField('Дата ответа', null=True, blank=True)
    
    # Метаданные
    created_at = models.DateTimeField('Получено', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_read(self):
        """Отметить как прочитанное"""
        if self.status == 'new':
            self.status = 'read'
            self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_replied(self, reply_text):
        """Отметить как отвеченное"""
        from django.utils import timezone
        self.reply_message = reply_text
        self.replied_at = timezone.now()
        self.status = 'replied'
        self.save(update_fields=['reply_message', 'replied_at', 'status', 'updated_at'])


class ContactInfo(models.Model):
    """Контактная информация для отображения на сайте"""
    
    # Основная информация
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=200, blank=True)
    
    # Социальные сети
    linkedin_url = models.URLField('LinkedIn', blank=True)
    github_url = models.URLField('GitHub', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    twitter_url = models.URLField('Twitter', blank=True)
    
    # Рабочие часы
    working_hours_en = models.CharField('Рабочие часы (EN)', max_length=100, blank=True)
    working_hours_ru = models.CharField('Рабочие часы (RU)', max_length=100, blank=True)
    working_hours_he = models.CharField('Рабочие часы (HE)', max_length=100, blank=True)
    
    # Доступность
    is_available_for_work = models.BooleanField('Доступен для работы', default=True)
    availability_note_en = models.TextField('Заметка о доступности (EN)', blank=True)
    availability_note_ru = models.TextField('Заметка о доступности (RU)', blank=True)
    availability_note_he = models.TextField('Заметка о доступности (HE)', blank=True)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'
        
    def __str__(self):
        return f"Контакты - {self.email}"