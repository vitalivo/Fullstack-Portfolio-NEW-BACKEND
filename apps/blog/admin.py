from django.contrib import admin
from .models import BlogCategory, BlogTag, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'name_he')
    search_fields = ('name_en', 'name_ru', 'name_he')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'author', 'status', 'is_featured', 'published_at', 'views_count')
    list_filter = ('status', 'is_featured', 'author', 'published_at')
    search_fields = ('title_en', 'title_ru', 'content_en')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('tags', 'categories')
    date_hierarchy = 'published_at'
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новый пост
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_en', 'title_ru', 'title_he', 'slug')
        }),
        ('Подзаголовки', {
            'fields': ('subtitle_en', 'subtitle_ru', 'subtitle_he'),
            'classes': ('collapse',)
        }),
        ('Краткие описания', {
            'fields': ('excerpt_en', 'excerpt_ru', 'excerpt_he')
        }),
        ('Контент', {
            'fields': ('content_en', 'content_ru', 'content_he')
        }),
        ('Изображения', {
            'fields': ('thumbnail', 'cover_image')
        }),
        ('Классификация', {
            'fields': ('categories', 'tags', 'status', 'is_featured')
        }),
        ('Публикация', {
            'fields': ('published_at', 'read_time')
        }),
        ('SEO', {
            'fields': ('meta_description_en', 'meta_description_ru', 'meta_description_he'),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
