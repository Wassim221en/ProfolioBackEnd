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
        'recommendation_date', 'is_featured', 'is_public', 'display_order'
    ]
    list_filter = [
        'is_featured', 'is_public', 'rating', 'recommendation_date',
        'recommender_company', 'relationship'
    ]
    search_fields = [
        'recommender_name', 'recommender_company', 'recommender_title',
        'recommendation_text', 'relationship', 'project_context'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at', 'short_recommendation']
    ordering = ['display_order', '-recommendation_date']

    fieldsets = (
        ('Recommender Information', {
            'fields': (
                'recommender_name', 'recommender_title', 'recommender_company',
                'recommender_location', 'recommender_image'
            )
        }),
        ('Recommendation Content', {
            'fields': (
                'recommendation_text', 'short_recommendation', 'relationship',
                'project_context', 'recommendation_date', 'rating'
            )
        }),
        ('Contact Information', {
            'fields': ('linkedin_url', 'email'),
            'classes': ('collapse',)
        }),
        ('Skills & Metadata', {
            'fields': ('skills_mentioned',),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_public', 'display_order')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['make_featured', 'remove_featured', 'make_public', 'make_private']

    def rating_stars(self, obj):
        """Display rating as stars."""
        return format_html(obj.get_rating_display())
    rating_stars.short_description = 'Rating'

    def make_featured(self, request, queryset):
        """Mark selected recommendations as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} recommendations marked as featured.')
    make_featured.short_description = 'Mark selected recommendations as featured'

    def remove_featured(self, request, queryset):
        """Remove featured status from selected recommendations."""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} recommendations removed from featured.')
    remove_featured.short_description = 'Remove featured status'

    def make_public(self, request, queryset):
        """Make selected recommendations public."""
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} recommendations made public.')
    make_public.short_description = 'Make selected recommendations public'

    def make_private(self, request, queryset):
        """Make selected recommendations private."""
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} recommendations made private.')
    make_private.short_description = 'Make selected recommendations private'
