from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import BlogCategory, BlogTag, BlogPost
from .serializers import BlogCategorySerializer, BlogTagSerializer, BlogPostSerializer, BlogPostListSerializer

class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий блога"""
    
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name_en', 'name_ru', 'name_he']

class BlogTagViewSet(viewsets.ReadOnlyModelViewSet):
    """API для тегов блога"""
    
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering = ['name']

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """API для постов блога"""
    
    queryset = BlogPost.objects.filter(status='published')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'tags', 'author', 'is_featured']
    search_fields = ['title_en', 'title_ru', 'title_he', 'excerpt_en', 'content_en']
    ordering_fields = ['published_at', 'views_count', 'read_time']
    ordering = ['-published_at']
    
    # ИСПРАВЛЕНО: Добавляем поддержку поиска по slug
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer
    
    # ИСПРАВЛЕНО: Переопределяем get_object для поиска по slug
    def get_object(self):
        """
        Получаем объект по slug вместо ID
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        slug = self.kwargs[lookup_url_kwarg]
        
        # Пытаемся найти по slug
        try:
            obj = get_object_or_404(self.get_queryset(), slug=slug)
            self.check_object_permissions(self.request, obj)
            return obj
        except:
            # Если не найден по slug, пытаемся найти по ID (для обратной совместимости)
            try:
                obj = get_object_or_404(self.get_queryset(), pk=slug)
                self.check_object_permissions(self.request, obj)
                return obj
            except:
                # Если ничего не найдено, возвращаем 404
                from django.http import Http404
                raise Http404("Blog post not found")
    
    def retrieve(self, request, *args, **kwargs):
        """Увеличиваем счетчик просмотров при получении поста"""
        instance = self.get_object()
        # ИСПРАВЛЕНО: Проверяем, есть ли метод increment_views
        if hasattr(instance, 'increment_views'):
            instance.increment_views()
        else:
            # Если метода нет, увеличиваем views_count напрямую
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные посты"""
        featured_posts = self.queryset.filter(is_featured=True)
        serializer = BlogPostListSerializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить посты по категории"""
        category_slug = request.query_params.get('category', None)
        if category_slug:
            posts = self.queryset.filter(categories__slug=category_slug)
            serializer = BlogPostListSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_tag(self, request):
        """Получить посты по тегу"""
        tag_slug = request.query_params.get('tag', None)
        if tag_slug:
            posts = self.queryset.filter(tags__slug=tag_slug)
            serializer = BlogPostListSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Tag parameter required'}, status=400)
