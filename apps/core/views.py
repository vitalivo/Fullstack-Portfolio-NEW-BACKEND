from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Profile, Experience
from .serializers import ProfileSerializer, ProfileWithExperienceSerializer, ExperienceSerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """API для профиля пользователя"""
    
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileWithExperienceSerializer
        return ProfileSerializer
    
    @action(detail=True, methods=['get'])
    def experiences(self, request, pk=None):
        """Получить опыт работы для профиля"""
        profile = self.get_object()
        experiences = profile.experiences.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API для опыта работы"""
    
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['experience_type', 'is_current']
    search_fields = ['company', 'position_en', 'position_ru', 'description_en']
    ordering_fields = ['start_date', 'end_date', 'order']
    ordering = ['-start_date', 'order']
