from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Technology, ProjectCategory, Project, ProjectImage
from .serializers import (
    TechnologySerializer, ProjectCategorySerializer, 
    ProjectSerializer, ProjectListSerializer, ProjectImageSerializer
)

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """API для технологий"""
    
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий проектов"""
    
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name_en', 'name_ru', 'name_he']

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API для проектов"""
    
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'project_type', 'is_featured', 'year', 'category']
    search_fields = ['title_en', 'title_ru', 'title_he', 'description_en', 'description_ru']
    ordering_fields = ['year', 'created_at', 'order']
    ordering = ['-is_featured', '-year', 'order']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить рекомендуемые проекты"""
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = ProjectListSerializer(featured_projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_technology(self, request):
        """Получить проекты по технологии"""
        tech_slug = request.query_params.get('tech', None)
        if tech_slug:
            projects = self.queryset.filter(technologies__slug=tech_slug)
            serializer = ProjectListSerializer(projects, many=True)
            return Response(serializer.data)
        return Response({'error': 'Technology parameter required'}, status=400)
    
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        """Получить изображения проекта"""
        project = self.get_object()
        images = project.images.all()
        serializer = ProjectImageSerializer(images, many=True)
        return Response(serializer.data)

class ProjectImageViewSet(viewsets.ReadOnlyModelViewSet):
    """API для изображений проектов"""
    
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project']
    ordering_fields = ['order']
    ordering = ['order']
