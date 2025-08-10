from rest_framework import serializers
from .models import BlogCategory, BlogTag, BlogPost

class BlogCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий блога"""
    
    class Meta:
        model = BlogCategory
        fields = [
            'id', 'name_en', 'name_ru', 'name_he', 'slug',
            'description_en', 'description_ru', 'description_he', 'color'
        ]

class BlogTagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов блога"""
    
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug', 'color']

class BlogPostSerializer(serializers.ModelSerializer):
    """Полный сериализатор для постов блога"""
    
    categories = BlogCategorySerializer(many=True, read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title_en', 'title_ru', 'title_he', 'slug',
            'subtitle_en', 'subtitle_ru', 'subtitle_he',
            'excerpt_en', 'excerpt_ru', 'excerpt_he',
            'content_en', 'content_ru', 'content_he',
            'thumbnail', 'cover_image', 'categories', 'tags',
            'author', 'author_name', 'status', 'status_display',
            'is_featured', 'published_at', 'read_time', 'views_count',
            'meta_description_en', 'meta_description_ru', 'meta_description_he',
            'created_at', 'updated_at'
        ]
        
        read_only_fields = ['author', 'views_count', 'created_at', 'updated_at']

class BlogPostListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка постов"""
    
    categories = BlogCategorySerializer(many=True, read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    # ИСПРАВЛЕНО: Добавляем определение поля status_display
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title_en', 'title_ru', 'title_he', 'slug',
            'subtitle_en', 'subtitle_ru', 'subtitle_he',
            'excerpt_en', 'excerpt_ru', 'excerpt_he',
            'thumbnail', 'categories', 'tags', 'author_name',
            'status', 'status_display',
            'is_featured', 'published_at', 'read_time', 'views_count',
            'meta_description_en', 'meta_description_ru', 'meta_description_he'
        ]
