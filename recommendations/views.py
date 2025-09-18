from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.shortcuts import get_object_or_404

from .models import Recommendation
from .serializers import (
    RecommendationSerializer,
    RecommendationListSerializer,
    RecommendationCreateSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_recommendation(request):
    """
    إنشاء توصية جديدة
    POST /api/recommendations/create/
    """
    serializer = RecommendationCreateSerializer(data=request.data)
    if serializer.is_valid():
        recommendation = serializer.save()
        # إرجاع البيانات الكاملة للتوصية المنشأة
        response_serializer = RecommendationSerializer(recommendation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_recommendations(request):
    """
    عرض جميع التوصيات
    GET /api/recommendations/
    """
    recommendations = Recommendation.objects.all().order_by('-recommendation_date')
    serializer = RecommendationListSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def recommendation_detail(request, pk):
    """
    عرض تفاصيل توصية محددة
    GET /api/recommendations/{id}/
    """
    recommendation = get_object_or_404(Recommendation, pk=pk)
    serializer = RecommendationSerializer(recommendation)
    return Response(serializer.data)
