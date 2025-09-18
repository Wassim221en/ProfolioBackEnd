from django.db import models
from django.core.validators import URLValidator
from common.models import BaseModel, RatingMixin
from common.managers import BaseManager
from common.utils import upload_to_directory
from django.core.validators import MinValueValidator, MaxValueValidator

def recommendation_image_upload_to(instance, filename):
    return upload_to_directory(instance, filename, 'recommendations/images')


class Recommendation(BaseModel, RatingMixin):
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
    recommendation_text = models.TextField(
        help_text="The actual recommendation text"
    )
    project_context = models.CharField(
        max_length=200,
        blank=True,
        help_text="Context or project where the collaboration happened"
    )
    linkedin_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="LinkedIn profile URL of the recommender"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email address of the recommender"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    recommendation_date = models.DateField(
        help_text="Date when the recommendation was given"
    )
    def __str__(self):
        return f"Recommendation from {self.recommender_name} ({self.recommender_company})"
    
    @property
    def short_recommendation(self):
        if len(self.recommendation_text) <= 150:
            return self.recommendation_text
        return self.recommendation_text[:150] + "..."

    @property
    def recommender_full_title(self):
        return f"{self.recommender_title} at {self.recommender_company}"