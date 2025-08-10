from django.contrib import admin
from .models import Technology, ProjectCategory, Project, ProjectImage

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'name_he')
    search_fields = ('name_en', 'name_ru', 'name_he')
    prepopulated_fields = {'slug': ('name_en',)}

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption_ru', 'order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'status', 'is_featured', 'year')
    list_filter = ('status', 'is_featured', 'project_type', 'year')
    search_fields = ('title_en', 'title_ru', 'description_en')
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ('technologies',)
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_en', 'title_ru', 'title_he', 'slug')
        }),
        ('Описание', {
            'fields': ('description_en', 'description_ru', 'description_he')
        }),
        ('Подробное описание', {
            'fields': ('long_description_en', 'long_description_ru', 'long_description_he'),
            'classes': ('collapse',)
        }),
        ('Классификация', {
            'fields': ('category', 'technologies', 'project_type', 'status', 'year')
        }),
        ('Ссылки', {
            'fields': ('github_url', 'demo_url', 'video_url')
        }),
        ('Изображения', {
            'fields': ('thumbnail', 'cover_image')
        }),
        ('Настройки', {
            'fields': ('is_featured', 'order')
        }),
    )
