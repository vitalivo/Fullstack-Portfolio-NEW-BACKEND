from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, ContactInfoViewSet

router = DefaultRouter()
router.register(r'messages', ContactMessageViewSet)
router.register(r'info', ContactInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
