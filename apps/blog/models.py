from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField

def get_default_author():
    """Получить автора по умолчанию (первый суперпользователь)"""
    try:
        return User.objects.filter(is_superuser=True).first().id
    except:
        return 1  # Fallback на ID=1

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
    title_en = models.CharField('Заголовок (EN)', max_length=200, blank=True)
    title_ru = models.CharField('Заголовок (RU)', max_length=200, blank=True)
    title_he = models.CharField('Заголовок (HE)', max_length=200, blank=True)
    slug = models.SlugField('Слаг', unique=True, blank=True)
    
    # Подзаголовки (опционально)
    subtitle_en = models.CharField('Подзаголовок (EN)', max_length=300, blank=True)
    subtitle_ru = models.CharField('Подзаголовок (RU)', max_length=300, blank=True)
    subtitle_he = models.CharField('Подзаголовок (HE)', max_length=300, blank=True)
    
    # Краткие описания для превью
    excerpt_en = models.TextField('Краткое описание (EN)', max_length=500, blank=True)
    excerpt_ru = models.TextField('Краткое описание (RU)', max_length=500, blank=True)
    excerpt_he = models.TextField('Краткое описание (HE)', max_length=500, blank=True)
    
    # Полный контент (с Rich Text Editor)
    content_en = models.TextField('Контент (EN)', blank=True)
    content_ru = models.TextField('Контент (RU)', blank=True)
    content_he = models.TextField('Контент (HE)', blank=True)
    
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
    
    # Метаданные - ИСПРАВЛЕНО: добавлен default для author
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор',
        default=get_default_author
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
        ordering = ['-published_at', '-created_at']
        
    def __str__(self):
        return self.title_ru or self.title_en or self.title_he or f"Пост #{self.id}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Создаем slug из первого доступного заголовка
            title_for_slug = self.title_en or self.title_ru or self.title_he or f"post-{self.id}"
            self.slug = slugify(title_for_slug)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

# Добавляем модель для предотвращения засыпания сайта
class KeepAlive(models.Model):
    """Модель для поддержания активности сайта"""
    
    last_ping = models.DateTimeField('Последний пинг', auto_now=True)
    is_active = models.BooleanField('Активен', default=True)
    ping_count = models.IntegerField('Количество пингов', default=0)
    
    class Meta:
        verbose_name = 'Keep Alive'
        verbose_name_plural = 'Keep Alive'
    
    def __str__(self):
        return f"Keep Alive - {self.last_ping}"
    
    @classmethod
    def ping(cls):
        """Обновить время последнего пинга"""
        obj, created = cls.objects.get_or_create(id=1)
        obj.ping_count += 1
        obj.save()
        return obj