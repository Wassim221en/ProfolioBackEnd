from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Recommendation
from .serializers import (
    RecommendationSerializer,
    RecommendationListSerializer,
    RecommendationCreateSerializer,
    RecommendationUpdateSerializer
)


class RecommendationViewSet(viewsets.ModelViewSet):
    """
    Ultra-simple ViewSet for managing recommendations.

    Available endpoints:
    - **GET /api/recommendations/**: List all recommendations (no pagination, search, or filters)
    - **POST /api/recommendations/**: Create a new recommendation
    - **GET /api/recommendations/{id}/**: Get recommendation details
    - **PUT /api/recommendations/{id}/**: Update recommendation
    """

    queryset = Recommendation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # No pagination
    http_method_names = ['get', 'post', 'put', 'head', 'options']  # Only allow these methods

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return RecommendationListSerializer
        elif self.action == 'create':
            return RecommendationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RecommendationUpdateSerializer
        return RecommendationSerializer

    def get_queryset(self):
        """Return all public recommendations - ultra simple."""
        return Recommendation.objects.filter(is_public=True).order_by('-recommendation_date')

    def create(self, request, *args, **kwargs):
        """Create a new recommendation - ultra simple."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing recommendation - ultra simple."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


