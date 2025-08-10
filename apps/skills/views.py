from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import SkillCategory, Skill
from .serializers import SkillCategorySerializer, SkillSerializer, SkillsByCategorySerializer

class SkillCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий навыков"""
    
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['order', 'name_en']
    ordering = ['order', 'name_en']
    
    @action(detail=False, methods=['get'])
    def with_skills(self, request):
        """Получить категории с навыками"""
        categories = self.queryset.prefetch_related('skills')
        serializer = SkillsByCategorySerializer(categories, many=True)
        return Response(serializer.data)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """API для навыков"""
    
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'category', 'skill_type', 'proficiency_level', 
        'is_featured', 'years_of_experience'
    ]
    search_fields = ['name', 'description_en', 'description_ru']
    ordering_fields = ['proficiency_percentage', 'years_of_experience', 'order']
    ordering = ['category', 'order', '-proficiency_percentage']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные навыки"""
        featured_skills = self.queryset.filter(is_featured=True)
        serializer = SkillSerializer(featured_skills, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить навыки по категории"""
        category_id = request.query_params.get('category', None)
        if category_id:
            skills = self.queryset.filter(category_id=category_id)
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Получить недавно используемые навыки"""
        recent_skills = [skill for skill in self.queryset.all() if skill.is_recent]
        serializer = SkillSerializer(recent_skills, many=True)
        return Response(serializer.data)
