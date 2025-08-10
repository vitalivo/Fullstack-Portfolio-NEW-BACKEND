from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    """Профиль пользователя - основная информация"""
    
    # Личная информация
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    birth_date = models.DateField('Дата рождения')
    location = models.CharField('Местоположение', max_length=100, default='Israel')
    
    # Контактная информация
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    linkedin_url = models.URLField('LinkedIn', blank=True)
    github_url = models.URLField('GitHub', blank=True)
    
    # Профессиональная информация (мультиязычная)
    current_title_en = models.CharField('Должность (EN)', max_length=200)
    current_title_ru = models.CharField('Должность (RU)', max_length=200)
    current_title_he = models.CharField('Должность (HE)', max_length=200)
    
    # Описание (мультиязычное)
    bio_en = models.TextField('Описание (EN)')
    bio_ru = models.TextField('Описание (RU)')
    bio_he = models.TextField('Описание (HE)')
    
    # Опыт работы
    years_management = models.IntegerField('Лет управленческого опыта', default=20)
    years_it = models.IntegerField('Лет в IT', default=2)
    team_size_managed = models.IntegerField('Размер управляемой команды', default=40)
    
    # Файлы
    photo = models.ImageField('Фото профиля', upload_to='profile/photos/', blank=True)
    resume_en = models.FileField('Резюме (EN)', upload_to='profile/resumes/', blank=True)
    resume_ru = models.FileField('Резюме (RU)', upload_to='profile/resumes/', blank=True)
    resume_he = models.FileField('Резюме (HE)', upload_to='profile/resumes/', blank=True)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class Experience(models.Model):
    """Опыт работы"""
    
    EXPERIENCE_TYPES = [
        ('management', 'Управление'),
        ('it', 'IT'),
        ('education', 'Образование'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    
    # Основная информация
    company = models.CharField('Компания', max_length=200)
    title_en = models.CharField('Должность (EN)', max_length=200)
    title_ru = models.CharField('Должность (RU)', max_length=200)
    title_he = models.CharField('Должность (HE)', max_length=200)
    
    # Даты
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    is_current = models.BooleanField('Текущая работа', default=False)
    
    # Описание (мультиязычное)
    description_en = models.TextField('Описание (EN)')
    description_ru = models.TextField('Описание (RU)')
    description_he = models.TextField('Описание (HE)')
    
    # Дополнительная информация
    experience_type = models.CharField('Тип опыта', max_length=20, choices=EXPERIENCE_TYPES)
    location = models.CharField('Местоположение', max_length=100)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-start_date', 'order']
        
    def __str__(self):
        return f"{self.company} - {self.title_ru}"