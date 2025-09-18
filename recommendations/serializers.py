from rest_framework import serializers
from common.serializers import BaseModelSerializer, RatingSerializer, DynamicFieldsModelSerializer
from .models import Recommendation


class RecommendationSerializer(BaseModelSerializer, RatingSerializer):
    recommender_full_title = serializers.ReadOnlyField()
    short_recommendation = serializers.ReadOnlyField()

    class Meta:
        model = Recommendation
        fields = [
            'id', 'created_at', 'updated_at',
            'recommender_name', 'recommender_title', 'recommender_company',
            'recommender_location', 'recommendation_text',
            'project_context', 'linkedin_url', 'email',
            'recommendation_date', 'rating',
            'recommender_full_title', 'short_recommendation'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'is_deleted', 'deleted_at',
            'recommender_full_title', 'short_recommendation'
        ]

    def validate_recommendation_text(self, value):
        """Validate recommendation text."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Recommendation text must be at least 10 characters long.")

        if len(value) > 2000:
            raise serializers.ValidationError("Recommendation text cannot exceed 2000 characters.")

        return value.strip()

    def validate_linkedin_url(self, value):
        """Validate LinkedIn URL."""
        if value and not (value.startswith('https://linkedin.com/') or value.startswith('https://www.linkedin.com/')):
            raise serializers.ValidationError("Please provide a valid LinkedIn profile URL.")
        return value


class RecommendationListSerializer(serializers.ModelSerializer):
    """
    Simple serializer for listing recommendations.
    """
    rating_stars = serializers.SerializerMethodField()
    short_recommendation = serializers.ReadOnlyField()

    class Meta:
        model = Recommendation
        fields = [
            'id',
            'recommender_name',
            'recommender_title',
            'recommender_company',
            'recommender_location',
            'recommendation_date',
            'rating',
            'rating_stars',
            'short_recommendation',
            'linkedin_url'
        ]

    def get_rating_stars(self, obj):
        """Return rating as stars."""
        return "★" * obj.rating + "☆" * (5 - obj.rating)


class RecommendationCreateSerializer(serializers.ModelSerializer):
    """
    Simple serializer for creating recommendations.
    """

    class Meta:
        model = Recommendation
        fields = [
            'recommender_name',
            'recommender_title',
            'recommender_company',
            'recommender_location',
            'recommendation_date',
            'rating',
            'recommendation_text',
            'project_context',
            'linkedin_url',
            'email'
        ]

    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_recommendation_text(self, value):
        """Validate recommendation text."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Recommendation text must be at least 10 characters long.")
        return value.strip()

    def validate_linkedin_url(self, value):
        """Validate LinkedIn URL format."""
        if value and not (value.startswith('https://linkedin.com/') or value.startswith('https://www.linkedin.com/')):
            raise serializers.ValidationError("Please provide a valid LinkedIn profile URL.")
        return value

