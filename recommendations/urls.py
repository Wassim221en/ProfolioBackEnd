from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet

app_name = 'recommendations'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
