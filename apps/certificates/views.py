from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Certificate
from .serializers import CertificateSerializer, CertificateListSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """API для сертификатов"""
    
    queryset = Certificate.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['certificate_type', 'issuer', 'is_featured', 'has_distinction']
    search_fields = ['title_en', 'title_ru', 'issuer', 'description_en']
    ordering_fields = ['issue_date', 'order']
    ordering = ['-issue_date', 'order']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CertificateListSerializer
        return CertificateSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные сертификаты"""
        featured_certs = self.queryset.filter(is_featured=True)
        serializer = CertificateListSerializer(featured_certs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Получить сертификаты по типу"""
        cert_type = request.query_params.get('type', None)
        if cert_type:
            certificates = self.queryset.filter(certificate_type=cert_type)
            serializer = CertificateListSerializer(certificates, many=True)
            return Response(serializer.data)
        return Response({'error': 'Type parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def with_distinction(self, request):
        """Получить сертификаты с отличием"""
        distinction_certs = self.queryset.filter(has_distinction=True)
        serializer = CertificateListSerializer(distinction_certs, many=True)
        return Response(serializer.data)
