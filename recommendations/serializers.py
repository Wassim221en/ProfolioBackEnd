from rest_framework import serializers
from common.serializers import BaseModelSerializer, RatingSerializer, DynamicFieldsModelSerializer
from .models import Recommendation


class RecommendationSerializer(BaseModelSerializer, RatingSerializer):
    """
    Full serializer for Recommendation model.
    """
    recommender_full_title = serializers.ReadOnlyField()
    short_recommendation = serializers.ReadOnlyField()
    skills_display = serializers.SerializerMethodField()
    recommender_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = [
            'id', 'created_at', 'updated_at', 'is_deleted', 'deleted_at',
            'recommender_name', 'recommender_title', 'recommender_company',
            'recommender_location', 'recommendation_text', 'relationship',
            'project_context', 'linkedin_url', 'email', 'recommender_image',
            'recommendation_date', 'is_featured', 'is_public', 'display_order',
            'skills_mentioned', 'rating', 'rating_display',
            'recommender_full_title', 'short_recommendation', 'skills_display',
            'recommender_image_url'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'is_deleted', 'deleted_at',
            'recommender_full_title', 'short_recommendation', 'rating_display',
            'skills_display', 'recommender_image_url'
        ]

    def get_skills_display(self, obj):
        """Return skills as a comma-separated string."""
        return obj.get_skills_display()

    def get_recommender_image_url(self, obj):
        """Return full URL for recommender image."""
        if obj.recommender_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.recommender_image.url)
            return obj.recommender_image.url
        return None

    def validate_skills_mentioned(self, value):
        """Validate skills mentioned field."""
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Skills must be provided as a list.")
        
        if value and len(value) > 20:
            raise serializers.ValidationError("Maximum 20 skills allowed.")
        
        # Clean up skills
        if value:
            cleaned_skills = []
            for skill in value:
                if isinstance(skill, str) and skill.strip():
                    cleaned_skills.append(skill.strip()[:50])  # Limit skill length
            return cleaned_skills
        
        return value

    def validate_recommendation_text(self, value):
        """Validate recommendation text."""
        if len(value.strip()) < 50:
            raise serializers.ValidationError("Recommendation text must be at least 50 characters long.")
        
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
    Ultra-simple serializer for listing recommendations.

    Format example:
    Ahmed Hassan
    Project Manager
    Tech Solutions Ltd
    Dubai, UAE
    June 20, 2024
    ★★★★★
    "Working with Wassim was a pleasure..."
    LinkedIn: https://linkedin.com/in/ahmed-hassan
    """
    rating_stars = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = [
            'id',
            'recommender_name',           # Ahmed Hassan
            'recommender_title',          # Project Manager
            'recommender_company',        # Tech Solutions Ltd
            'recommender_location',       # Dubai, UAE
            'recommendation_date',        # June 20, 2024
            'rating',                     # 5
            'rating_stars',              # ★★★★★
            'recommendation_text',        # "Working with Wassim was..."
            'linkedin_url'               # LinkedIn profile URL
        ]

    def get_rating_stars(self, obj):
        """Return rating as stars."""
        return "★" * obj.rating + "☆" * (5 - obj.rating)


class RecommendationCreateSerializer(serializers.ModelSerializer):
    """
    Ultra-simple serializer for creating recommendations.
    Only essential fields required.
    """

    class Meta:
        model = Recommendation
        fields = [
            'recommender_name',        # Required: Ahmed Hassan
            'recommender_title',       # Required: Project Manager
            'recommender_company',     # Required: Tech Solutions Ltd
            'recommender_location',    # Optional: Dubai, UAE
            'recommendation_date',     # Required: 2024-06-20
            'rating',                  # Required: 5 (1-5 stars)
            'recommendation_text',     # Required: "Working with Wassim..."
            'linkedin_url'             # Optional: LinkedIn profile URL
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


class RecommendationUpdateSerializer(serializers.ModelSerializer):
    """
    Ultra-simple serializer for updating recommendations.
    Same fields as create.
    """

    class Meta:
        model = Recommendation
        fields = [
            'recommender_name',        # Ahmed Hassan
            'recommender_title',       # Project Manager
            'recommender_company',     # Tech Solutions Ltd
            'recommender_location',    # Dubai, UAE
            'recommendation_date',     # 2024-06-20
            'rating',                  # 5 (1-5 stars)
            'recommendation_text',     # "Working with Wassim..."
            'linkedin_url'             # LinkedIn profile URL
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


