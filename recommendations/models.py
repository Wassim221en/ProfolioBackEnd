from django.db import models
from django.core.validators import URLValidator
from common.models import BaseModel, RatingMixin
from common.managers import BaseManager
from common.utils import upload_to_directory


def recommendation_image_upload_to(instance, filename):
    """Upload path for recommendation images."""
    return upload_to_directory(instance, filename, 'recommendations/images')


class Recommendation(BaseModel, RatingMixin):
    """
    Model representing a professional recommendation.
    """
    # Personal Information
    recommender_name = models.CharField(
        max_length=100,
        help_text="Full name of the person giving the recommendation"
    )

    recommender_title = models.CharField(
        max_length=150,
        help_text="Professional title of the recommender"
    )

    recommender_company = models.CharField(
        max_length=100,
        help_text="Company or organization of the recommender"
    )

    recommender_location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Location of the recommender"
    )

    # Recommendation Content
    recommendation_text = models.TextField(
        help_text="The actual recommendation text"
    )

    # Professional Details
    relationship = models.CharField(
        max_length=100,
        help_text="Professional relationship (e.g., 'Direct Manager', 'Colleague', 'Client')"
    )

    project_context = models.CharField(
        max_length=200,
        blank=True,
        help_text="Context or project where the collaboration happened"
    )

    # Contact Information
    linkedin_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="LinkedIn profile URL of the recommender"
    )

    email = models.EmailField(
        blank=True,
        help_text="Email address of the recommender"
    )

    # Media
    recommender_image = models.ImageField(
        upload_to=recommendation_image_upload_to,
        blank=True,
        null=True,
        help_text="Profile image of the recommender"
    )

    # Metadata
    recommendation_date = models.DateField(
        help_text="Date when the recommendation was given"
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="Whether this recommendation should be featured prominently"
    )

    is_public = models.BooleanField(
        default=True,
        help_text="Whether this recommendation is publicly visible"
    )

    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order for displaying recommendations (lower numbers first)"
    )

    # Skills mentioned in the recommendation
    skills_mentioned = models.JSONField(
        default=list,
        blank=True,
        help_text="List of skills mentioned in the recommendation"
    )

    # Manager
    objects = BaseManager()

    class Meta:
        ordering = ['display_order', '-recommendation_date', '-created_at']
        indexes = [
            models.Index(fields=['is_public', 'is_featured']),
            models.Index(fields=['recommendation_date']),
            models.Index(fields=['display_order']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"Recommendation from {self.recommender_name} ({self.recommender_company})"

    @property
    def short_recommendation(self):
        """Return a shortened version of the recommendation text."""
        if len(self.recommendation_text) <= 150:
            return self.recommendation_text
        return self.recommendation_text[:150] + "..."

    @property
    def recommender_full_title(self):
        """Return full title with company."""
        return f"{self.recommender_title} at {self.recommender_company}"

    def get_skills_display(self):
        """Return skills as a comma-separated string."""
        if isinstance(self.skills_mentioned, list):
            return ", ".join(self.skills_mentioned)
        return ""
