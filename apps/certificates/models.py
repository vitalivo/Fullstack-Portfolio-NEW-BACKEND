from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Certificate(models.Model):
    """Сертификаты и достижения"""
    CERTIFICATE_TYPES = [
        ('course', 'Курс'),
        ('certification', 'Сертификация'),
        ('diploma', 'Диплом'),
        ('achievement', 'Достижение'),
    ]
    
    # Основная информация (мультиязычная)
    title_en = models.CharField('Название (EN)', max_length=200)
    title_ru = models.CharField('Название (RU)', max_length=200, blank=True)
    title_he = models.CharField('Название (HE)', max_length=200, blank=True)
    
    # Организация и ID
    issuer = models.CharField('Организация', max_length=200)
    credential_id = models.CharField('ID сертификата', max_length=100, blank=True)
    
    # Даты
    issue_date = models.DateField('Дата выдачи')
    expiry_date = models.DateField('Дата истечения', null=True, blank=True)
    
    # Описание (мультиязычное)
    description_en = models.TextField('Описание (EN)', blank=True)
    description_ru = models.TextField('Описание (RU)', blank=True)
    description_he = models.TextField('Описание (HE)', blank=True)
    
    # Навыки (мультиязычные)
    skills_learned_en = models.TextField('Изученные навыки (EN)', blank=True, help_text='Перечислите через запятую')
    skills_learned_ru = models.TextField('Изученные навыки (RU)', blank=True, help_text='Перечислите через запятую')
    skills_learned_he = models.TextField('Изученные навыки (HE)', blank=True, help_text='Перечислите через запятую')
    
    # Файлы и ссылки
    certificate_image = models.ImageField('Изображение сертификата', upload_to='certificates/')
    verify_url = models.URLField('Ссылка для проверки', blank=True)
    certificate_file = models.FileField('Файл сертификата', upload_to='certificates/files/', blank=True)
    
    # Дополнительная информация
    certificate_type = models.CharField('Тип сертификата', max_length=20, choices=CERTIFICATE_TYPES)
    
    # Оценка и отличия
    score = models.CharField('Оценка', max_length=20, blank=True, help_text='Например: 100%, A+, 5.0')
    has_distinction = models.BooleanField('С отличием', default=False)
    
    # Отображение
    is_featured = models.BooleanField('Показывать на главной', default=False)
    order = models.IntegerField('Порядок отображения', default=0)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['-issue_date', 'order']
    
    def __str__(self):
        return f"{self.title_en} - {self.issuer}"
    
    @property
    def is_expired(self):
        """Проверка истечения сертификата"""
        if self.expiry_date:
            from datetime import date
            return date.today() > self.expiry_date
        return False
    
    def get_skills_list_en(self):
        """Получить список навыков (EN) как массив"""
        if self.skills_learned_en:
            return [skill.strip() for skill in self.skills_learned_en.split(',')]
        return []
    
    def get_skills_list_ru(self):
        """Получить список навыков (RU) как массив"""
        if self.skills_learned_ru:
            return [skill.strip() for skill in self.skills_learned_ru.split(',')]
        return []
    
    def get_skills_list_he(self):
        """Получить список навыков (HE) как массив"""
        if self.skills_learned_he:
            return [skill.strip() for skill in self.skills_learned_he.split(',')]
        return []
