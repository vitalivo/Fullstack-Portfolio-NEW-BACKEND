from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SkillCategory(models.Model):
    """Категории навыков"""
    
    name_en = models.CharField('Название (EN)', max_length=100)
    name_ru = models.CharField('Название (RU)', max_length=100)
    name_he = models.CharField('Название (HE)', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    icon = models.CharField('Иконка', max_length=100, blank=True, help_text='CSS класс иконки')
    color = models.CharField('Цвет', max_length=7, default='#3B82F6')
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Категория навыков'
        verbose_name_plural = 'Категории навыков'
        ordering = ['order', 'name_ru']
        
    def __str__(self):
        return self.name_ru


class Skill(models.Model):
    """Навыки и технологии"""
    
    SKILL_TYPES = [
        ('technical', 'Технический'),
        ('soft', 'Гибкий навык'),
        ('language', 'Язык'),
        ('tool', 'Инструмент'),
    ]
    
    PROFICIENCY_LEVELS = [
        (1, 'Начинающий'),
        (2, 'Базовый'),
        (3, 'Средний'),
        (4, 'Продвинутый'),
        (5, 'Эксперт'),
    ]
    
    # Основная информация
    name = models.CharField('Название', max_length=100)
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE, verbose_name='Категория')
    skill_type = models.CharField('Тип навыка', max_length=20, choices=SKILL_TYPES, default='technical')
    
    # Уровень владения
    proficiency_level = models.IntegerField(
        'Уровень владения',
        choices=PROFICIENCY_LEVELS,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    proficiency_percentage = models.IntegerField(
        'Процент владения',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50,
        help_text='От 0 до 100%'
    )
    
    # Дополнительная информация
    description_en = models.TextField('Описание (EN)', blank=True)
    description_ru = models.TextField('Описание (RU)', blank=True)
    description_he = models.TextField('Описание (HE)', blank=True)
    
    # Опыт
    years_of_experience = models.FloatField('Лет опыта', default=0.0)
    last_used = models.DateField('Последнее использование', null=True, blank=True)
    
    # Визуальное отображение
    icon = models.CharField('Иконка', max_length=100, blank=True)
    color = models.CharField('Цвет', max_length=7, blank=True)
    logo = models.ImageField('Логотип', upload_to='skills/logos/', blank=True)
    
    # Сертификации и проекты
    related_certificates = models.ManyToManyField(
        'certificates.Certificate',
        blank=True,
        verbose_name='Связанные сертификаты'
    )
    
    # Отображение
    is_featured = models.BooleanField('Показывать на главной', default=True)
    order = models.IntegerField('Порядок в категории', default=0)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['category', 'order', '-proficiency_percentage']
        unique_together = ['name', 'category']
        
    def __str__(self):
        return f"{self.name} ({self.category.name_ru})"
    
    def get_proficiency_text(self):
        """Получить текстовое описание уровня"""
        return dict(self.PROFICIENCY_LEVELS)[self.proficiency_level]
    
    @property
    def is_recent(self):
        """Проверка, использовался ли навык недавно"""
        if self.last_used:
            from datetime import date, timedelta
            return date.today() - self.last_used <= timedelta(days=365)
        return True