from django.db import models
from django.utils.text import slugify

class Technology(models.Model):
    """Технологии для проектов"""
    
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    color = models.CharField('Цвет', max_length=7, default='#3B82F6', help_text='HEX цвет для отображения')
    icon = models.CharField('Иконка', max_length=100, blank=True, help_text='CSS класс иконки')
    
    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProjectCategory(models.Model):
    """Категории проектов"""
    
    name_en = models.CharField('Название (EN)', max_length=100)
    name_ru = models.CharField('Название (RU)', max_length=100)
    name_he = models.CharField('Название (HE)', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    
    class Meta:
        verbose_name = 'Категория проекта'
        verbose_name_plural = 'Категории проектов'
        
    def __str__(self):
        return self.name_ru


class Project(models.Model):
    """Проекты портфолио"""
    
    STATUS_CHOICES = [
        ('completed', 'Завершен'),
        ('in_progress', 'В разработке'),
        ('live', 'Запущен'),
        ('archived', 'Архивирован'),
    ]
    
    TYPE_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Full-Stack'),
        ('mobile', 'Mobile'),
        ('desktop', 'Desktop'),
    ]
    
    # Основная информация (мультиязычная)
    title_en = models.CharField('Название (EN)', max_length=200)
    title_ru = models.CharField('Название (RU)', max_length=200)
    title_he = models.CharField('Название (HE)', max_length=200)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    
    # Описания (мультиязычные)
    description_en = models.TextField('Краткое описание (EN)')
    description_ru = models.TextField('Краткое описание (RU)')
    description_he = models.TextField('Краткое описание (HE)')
    
    long_description_en = models.TextField('Подробное описание (EN)', blank=True)
    long_description_ru = models.TextField('Подробное описание (RU)', blank=True)
    long_description_he = models.TextField('Подробное описание (HE)', blank=True)
    
    # Ссылки
    github_url = models.URLField('GitHub URL', blank=True)
    demo_url = models.URLField('Demo URL', blank=True)
    video_url = models.URLField('Video URL', blank=True)
    
    # Изображения
    thumbnail = models.ImageField('Миниатюра', upload_to='projects/thumbnails/', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='projects/covers/', blank=True)
    
    # Классификация
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    technologies = models.ManyToManyField(Technology, verbose_name='Технологии', blank=True)
    project_type = models.CharField('Тип проекта', max_length=20, choices=TYPE_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Дополнительная информация
    year = models.IntegerField('Год создания')
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    order = models.IntegerField('Порядок отображения', default=0)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-is_featured', '-year', 'order']
        
    def __str__(self):
        return self.title_ru
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    """Дополнительные изображения проектов"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='projects/gallery/')
    caption_en = models.CharField('Подпись (EN)', max_length=200, blank=True)
    caption_ru = models.CharField('Подпись (RU)', max_length=200, blank=True)
    caption_he = models.CharField('Подпись (HE)', max_length=200, blank=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проектов'
        ordering = ['order']
        
    def __str__(self):
        return f"{self.project.title_ru} - Изображение {self.order}"