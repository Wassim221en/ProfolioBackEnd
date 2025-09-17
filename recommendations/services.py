from typing import Dict, List, Any, Optional
from datetime import datetime, date
from django.core.files.uploadedfile import UploadedFile
from common.services import DjangoService
from common.exceptions import ValidationError, BusinessLogicError
from common.utils import safe_delete_file, validate_image_file
from .repositories import RecommendationRepository
from .models import Recommendation


class RecommendationService(DjangoService):
    """
    Service class for handling Recommendation business logic.
    """

    def __init__(self):
        repository = RecommendationRepository()
        super().__init__(repository)
        # Initialize logger explicitly
        import logging
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_business_rules(self, data: Dict[str, Any]) -> None:
        """
        Validate business rules for recommendations.
        
        Args:
            data: Recommendation data
            
        Raises:
            ValidationError: If validation fails
            BusinessLogicError: If business rules are violated
        """
        # Validate required fields
        required_fields = [
            'recommender_name', 'recommender_title', 'recommender_company',
            'recommendation_text', 'relationship', 'recommendation_date', 'rating'
        ]
        self.validate_data(data, required_fields)

        # Validate rating
        rating = data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise ValidationError("Rating must be between 1 and 5")

        # Validate recommendation date
        recommendation_date = data.get('recommendation_date')
        if recommendation_date and isinstance(recommendation_date, date):
            if recommendation_date > date.today():
                raise ValidationError("Recommendation date cannot be in the future")

        # Validate recommendation text length
        recommendation_text = data.get('recommendation_text', '')
        if len(recommendation_text) < 50:
            raise ValidationError("Recommendation text must be at least 50 characters long")

        # Validate LinkedIn URL format
        linkedin_url = data.get('linkedin_url')
        if linkedin_url and not linkedin_url.startswith('https://linkedin.com/'):
            if not linkedin_url.startswith('https://www.linkedin.com/'):
                raise ValidationError("LinkedIn URL must be a valid LinkedIn profile URL")

        # Validate skills format
        skills_mentioned = data.get('skills_mentioned')
        if skills_mentioned and not isinstance(skills_mentioned, list):
            raise ValidationError("Skills mentioned must be a list")

    def create_recommendation(self, data: Dict[str, Any]) -> Recommendation:
        """
        Create a new recommendation with business logic.
        
        Args:
            data: Recommendation data
            
        Returns:
            Created recommendation
        """
        # Process skills if provided as string
        if 'skills_mentioned' in data and isinstance(data['skills_mentioned'], str):
            data['skills_mentioned'] = [skill.strip() for skill in data['skills_mentioned'].split(',') if skill.strip()]

        # Set default display order if not provided
        if 'display_order' not in data:
            from django.db import models
            max_order = self.repository.get_all().aggregate(
                max_order=models.Max('display_order')
            )['max_order'] or 0
            data['display_order'] = max_order + 1

        return self.create(data)

    def update_recommendation(self, recommendation_id: str, data: Dict[str, Any]) -> Recommendation:
        """
        Update a recommendation with business logic.
        
        Args:
            recommendation_id: Recommendation ID
            data: Updated data
            
        Returns:
            Updated recommendation
        """
        # Process skills if provided as string
        if 'skills_mentioned' in data and isinstance(data['skills_mentioned'], str):
            data['skills_mentioned'] = [skill.strip() for skill in data['skills_mentioned'].split(',') if skill.strip()]

        return self.update(recommendation_id, data)

    def upload_recommender_image(self, recommendation_id: str, image_file: UploadedFile) -> Recommendation:
        """
        Upload and associate an image with a recommendation.
        
        Args:
            recommendation_id: Recommendation ID
            image_file: Uploaded image file
            
        Returns:
            Updated recommendation
            
        Raises:
            ValidationError: If image is invalid
        """
        # Validate image
        if not validate_image_file(image_file):
            raise ValidationError("Invalid image file")

        # Get recommendation
        recommendation = self.get_by_id(recommendation_id)

        # Delete old image if exists
        if recommendation.recommender_image:
            safe_delete_file(recommendation.recommender_image.path)

        # Update with new image
        return self.update(recommendation_id, {'recommender_image': image_file})

    def get_public_recommendations(self, filters: Optional[Dict] = None) -> List[Recommendation]:
        """
        Get public recommendations with optional filters.
        
        Args:
            filters: Optional filters
            
        Returns:
            List of public recommendations
        """
        if filters:
            return list(self.repository.get_public_recommendations().filter(**filters))
        return list(self.repository.get_public_recommendations())

    def get_featured_recommendations(self) -> List[Recommendation]:
        """
        Get featured recommendations.
        
        Returns:
            List of featured recommendations
        """
        return list(self.repository.get_featured_recommendations())

    def search_recommendations(self, query: str, filters: Optional[Dict] = None) -> List[Recommendation]:
        """
        Search recommendations with optional filters.
        
        Args:
            query: Search query
            filters: Optional additional filters
            
        Returns:
            List of matching recommendations
        """
        results = self.repository.search_recommendations(query)
        
        if filters:
            results = results.filter(**filters)
        
        return list(results)

    def get_recommendations_by_rating(self, min_rating: int = 1, max_rating: int = 5) -> List[Recommendation]:
        """
        Get recommendations by rating range.
        
        Args:
            min_rating: Minimum rating
            max_rating: Maximum rating
            
        Returns:
            List of recommendations within rating range
        """
        return list(self.repository.get_by_rating(min_rating, max_rating))

    def get_recommendations_by_company(self, company_name: str) -> List[Recommendation]:
        """
        Get recommendations from a specific company.
        
        Args:
            company_name: Company name
            
        Returns:
            List of recommendations from the company
        """
        return list(self.repository.get_by_company(company_name))

    def get_recommendations_by_skills(self, skills: List[str]) -> List[Recommendation]:
        """
        Get recommendations mentioning specific skills.
        
        Args:
            skills: List of skills
            
        Returns:
            List of recommendations mentioning the skills
        """
        return list(self.repository.get_by_skills(skills))

    def get_latest_recommendations(self, limit: int = 5) -> List[Recommendation]:
        """
        Get latest recommendations.
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            List of latest recommendations
        """
        return list(self.repository.get_latest_recommendations(limit))

    def get_highest_rated_recommendations(self, limit: int = 5) -> List[Recommendation]:
        """
        Get highest rated recommendations.
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            List of highest rated recommendations
        """
        return list(self.repository.get_highest_rated_recommendations(limit))

    def get_recommendations_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about recommendations.
        
        Returns:
            Dictionary with recommendation statistics
        """
        return self.repository.get_recommendations_stats()

    def toggle_featured_status(self, recommendation_id: str) -> Recommendation:
        """
        Toggle featured status of a recommendation.
        
        Args:
            recommendation_id: Recommendation ID
            
        Returns:
            Updated recommendation
        """
        recommendation = self.repository.toggle_featured_status(recommendation_id)
        
        # Clear cache
        self.delete_cache(f"by_id:{recommendation_id}")
        self.clear_related_cache(['all', 'featured'])
        
        self.log_operation('toggle_featured', recommendation_id, 
                          {'is_featured': recommendation.is_featured})
        
        return recommendation

    def toggle_public_status(self, recommendation_id: str) -> Recommendation:
        """
        Toggle public status of a recommendation.
        
        Args:
            recommendation_id: Recommendation ID
            
        Returns:
            Updated recommendation
        """
        recommendation = self.get_by_id(recommendation_id)
        new_status = not recommendation.is_public
        
        return self.update(recommendation_id, {'is_public': new_status})

    def update_display_order(self, recommendations_order: List[Dict[str, Any]]) -> bool:
        """
        Update display order for multiple recommendations.
        
        Args:
            recommendations_order: List of dicts with 'id' and 'order' keys
            
        Returns:
            True if updated successfully
        """
        result = self.repository.update_display_order(recommendations_order)
        
        # Clear all related caches
        self.clear_related_cache(['all', 'featured', 'public'])
        
        self.log_operation('update_display_order', 
                          extra_data={'count': len(recommendations_order)})
        
        return result

    def get_companies_list(self) -> List[str]:
        """
        Get list of companies that provided recommendations.
        
        Returns:
            List of company names
        """
        cache_key = "companies_list"
        cached_data = self.get_from_cache(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        companies = self.repository.get_companies_list()
        self.set_cache(cache_key, companies, timeout=3600)  # Cache for 1 hour
        
        return companies

    def get_skills_list(self) -> List[str]:
        """
        Get list of all skills mentioned in recommendations.
        
        Returns:
            List of unique skills
        """
        cache_key = "skills_list"
        cached_data = self.get_from_cache(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        skills = self.repository.get_skills_list()
        self.set_cache(cache_key, skills, timeout=3600)  # Cache for 1 hour
        
        return skills
