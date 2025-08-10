from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField

class BlogCategory(models.Model):
    """Категории блога"""
    
    name_en = models.CharField('Название (EN)', max_length=100)
    name_ru = models.CharField('Название (RU)', max_length=100)
    name_he = models.CharField('Название (HE)', max_length=100)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    description_en = models.TextField('Описание (EN)', blank=True)
    description_ru = models.TextField('Описание (RU)', blank=True)
    description_he = models.TextField('Описание (HE)', blank=True)
    color = models.CharField('Цвет', max_length=7, default='#3B82F6')
    
    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'
        ordering = ['name_ru']
        
    def __str__(self):
        return self.name_ru
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    """Теги блога"""
    
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    color = models.CharField('Цвет', max_length=7, default='#6B7280')
    
    class Meta:
        verbose_name = 'Тег блога'
        verbose_name_plural = 'Теги блога'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Посты блога"""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архивирован'),
    ]
    
    # Основная информация (мультиязычная)
    title_en = models.CharField('Заголовок (EN)', max_length=200)
    title_ru = models.CharField('Заголовок (RU)', max_length=200)
    title_he = models.CharField('Заголовок (HE)', max_length=200)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    
    # Подзаголовки (опционально)
    subtitle_en = models.CharField('Подзаголовок (EN)', max_length=300, blank=True)
    subtitle_ru = models.CharField('Подзаголовок (RU)', max_length=300, blank=True)
    subtitle_he = models.CharField('Подзаголовок (HE)', max_length=300, blank=True)
    
    # Краткие описания для превью
    excerpt_en = models.TextField('Краткое описание (EN)', max_length=500)
    excerpt_ru = models.TextField('Краткое описание (RU)', max_length=500)
    excerpt_he = models.TextField('Краткое описание (HE)', max_length=500)
    
    # Полный контент (с Rich Text Editor)
    content_en = models.TextField('Контент (EN)')  # Вместо RichTextField
    content_ru = models.TextField('Контент (RU)')  # Вместо RichTextField  
    content_he = models.TextField('Контент (HE)')  # Вместо RichTextField
    
    # Изображения
    thumbnail = models.ImageField('Миниатюра', upload_to='blog/thumbnails/', blank=True)
    cover_image = models.ImageField('Обложка', upload_to='blog/covers/', blank=True)
    
    # Классификация
    categories = models.ManyToManyField(BlogCategory, verbose_name='Категории', blank=True)
    tags = models.ManyToManyField(BlogTag, verbose_name='Теги', blank=True)
    
    # Публикация
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    published_at = models.DateTimeField('Дата публикации', null=True, blank=True)
    
    # SEO
    meta_description_en = models.CharField('Meta описание (EN)', max_length=160, blank=True)
    meta_description_ru = models.CharField('Meta описание (RU)', max_length=160, blank=True)
    meta_description_he = models.CharField('Meta описание (HE)', max_length=160, blank=True)
    
    # Статистика
    read_time = models.IntegerField('Время чтения (мин)', default=5)
    views_count = models.IntegerField('Просмотры', default=0)
    
    # Метаданные
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
        ordering = ['-published_at', '-created_at']
        
    def __str__(self):
        return self.title_ru
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])