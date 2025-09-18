from django.contrib import admin
from django.utils.html import format_html
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """
    Admin interface for Recommendation model.
    """
    list_display = [
        'recommender_name', 'recommender_company', 'rating_stars',
        'recommendation_date', 'rating'
    ]
    list_filter = [
        'rating', 'recommendation_date', 'recommender_company'
    ]
    search_fields = [
        'recommender_name', 'recommender_company', 'recommender_title',
        'recommendation_text', 'project_context'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at', 'short_recommendation']
    ordering = ['-recommendation_date']

    fieldsets = (
        ('Recommender Information', {
            'fields': (
                'recommender_name', 'recommender_title', 'recommender_company',
                'recommender_location'
            )
        }),
        ('Recommendation Content', {
            'fields': (
                'recommendation_text', 'short_recommendation',
                'project_context', 'recommendation_date', 'rating'
            )
        }),
        ('Contact Information', {
            'fields': ('linkedin_url', 'email'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def rating_stars(self, obj):
        """Display rating as stars."""
        return "★" * obj.rating + "☆" * (5 - obj.rating)
    rating_stars.short_description = 'Rating'
