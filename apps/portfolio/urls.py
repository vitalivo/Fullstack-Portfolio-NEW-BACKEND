from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnologyViewSet, ProjectCategoryViewSet, ProjectViewSet, ProjectImageViewSet

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet)
router.register(r'categories', ProjectCategoryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-images', ProjectImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
