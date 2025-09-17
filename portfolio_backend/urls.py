"""
URL configuration for portfolio_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Portfolio Backend API",
        default_version='v1',
        description="""
        # Portfolio Backend API Documentation

        This is a comprehensive Django REST API for managing professional recommendations.

        ## Features
        - Professional recommendations management
        - Rating system (1-5 stars)
        - Skills tracking
        - Image uploads
        - Featured recommendations
        - Advanced search and filtering
        - Statistics and analytics

        ## Architecture
        - Repository Pattern for data access
        - Service Layer for business logic
        - Common layer for shared utilities
        - Comprehensive caching system
        - Advanced error handling

        ## Authentication
        Currently using Django session authentication.
        Future versions will include JWT token authentication.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="Wassim Alshami",
            email="wassim.alshami@example.com",
            url="https://www.linkedin.com/in/wassim-alshami"
        ),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('', include('recommendations.urls', namespace='recommendations')),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),

    # API Routes
    path('api/', include('recommendations.urls', namespace='recommendations')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
