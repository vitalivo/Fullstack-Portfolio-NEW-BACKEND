from rest_framework import serializers
from .models import Technology, ProjectCategory, Project, ProjectImage

class TechnologySerializer(serializers.ModelSerializer):
    """Сериализатор для технологий"""
    
    class Meta:
        model = Technology
        fields = ['id', 'name', 'slug', 'color', 'icon']

class ProjectCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий проектов"""
    
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name_en', 'name_ru', 'name_he', 'slug']

class ProjectImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений проектов"""
    
    class Meta:
        model = ProjectImage
        fields = [
            'id', 'image', 'caption_en', 'caption_ru', 'caption_he', 'order'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    """Полный сериализатор для проектов"""
    
    category = ProjectCategorySerializer(read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title_en', 'title_ru', 'title_he', 'slug',
            'description_en', 'description_ru', 'description_he',
            'long_description_en', 'long_description_ru', 'long_description_he',
            'github_url', 'demo_url', 'video_url',
            'thumbnail', 'cover_image', 'category', 'technologies',
            'project_type', 'type_display', 'status', 'status_display',
            'year', 'is_featured', 'order', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProjectListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка проектов"""
    
    category = ProjectCategorySerializer(read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title_en', 'title_ru', 'title_he', 'slug',
            'description_en', 'description_ru', 'description_he',
            # ИСПРАВЛЕНО: Добавляем URL поля в список проектов
            'github_url', 'demo_url', 'video_url',
            'thumbnail', 'category', 'technologies',
            'project_type', 'type_display', 'status', 'status_display',
            'year', 'is_featured', 'created_at'
        ]
