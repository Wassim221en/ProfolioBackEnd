from typing import List, Optional, Dict, Any
from django.db.models import QuerySet, Q, Avg
from common.repositories import DjangoRepository
from .models import Recommendation


class RecommendationRepository(DjangoRepository):
    """
    Repository for handling Recommendation data access operations.
    """

    def __init__(self):
        super().__init__(Recommendation)

    def get_public_recommendations(self) -> QuerySet:
        """
        Get all public recommendations.
        
        Returns:
            QuerySet of public recommendations
        """
        return self.filter_by(is_public=True)

    def get_featured_recommendations(self) -> QuerySet:
        """
        Get featured recommendations.
        
        Returns:
            QuerySet of featured recommendations
        """
        return self.filter_by(is_public=True, is_featured=True)

    def get_by_rating(self, min_rating: int = 1, max_rating: int = 5) -> QuerySet:
        """
        Get recommendations by rating range.
        
        Args:
            min_rating: Minimum rating (1-5)
            max_rating: Maximum rating (1-5)
            
        Returns:
            QuerySet of recommendations within rating range
        """
        return self.filter_by(
            is_public=True,
            rating__gte=min_rating,
            rating__lte=max_rating
        )

    def get_by_company(self, company_name: str) -> QuerySet:
        """
        Get recommendations from a specific company.
        
        Args:
            company_name: Name of the company
            
        Returns:
            QuerySet of recommendations from the company
        """
        return self.filter_by(
            is_public=True,
            recommender_company__icontains=company_name
        )

    def get_by_skills(self, skills: List[str]) -> QuerySet:
        """
        Get recommendations that mention specific skills.
        
        Args:
            skills: List of skills to search for
            
        Returns:
            QuerySet of recommendations mentioning the skills
        """
        q_objects = Q()
        for skill in skills:
            q_objects |= Q(skills_mentioned__icontains=skill)
        
        return self.filter_by(is_public=True).filter(q_objects)

    def search_recommendations(self, query: str) -> QuerySet:
        """
        Search recommendations by text content.
        
        Args:
            query: Search query
            
        Returns:
            QuerySet of matching recommendations
        """
        return self.filter_by(is_public=True).filter(
            Q(recommendation_text__icontains=query) |
            Q(recommender_name__icontains=query) |
            Q(recommender_company__icontains=query) |
            Q(recommender_title__icontains=query) |
            Q(relationship__icontains=query) |
            Q(project_context__icontains=query)
        )

    def get_recommendations_by_date_range(self, start_date, end_date) -> QuerySet:
        """
        Get recommendations within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            QuerySet of recommendations within date range
        """
        return self.filter_by(
            is_public=True,
            recommendation_date__gte=start_date,
            recommendation_date__lte=end_date
        )

    def get_latest_recommendations(self, limit: int = 5) -> QuerySet:
        """
        Get the latest recommendations.
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            QuerySet of latest recommendations
        """
        return self.get_public_recommendations().order_by('-recommendation_date')[:limit]

    def get_highest_rated_recommendations(self, limit: int = 5) -> QuerySet:
        """
        Get the highest rated recommendations.
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            QuerySet of highest rated recommendations
        """
        return self.get_public_recommendations().order_by('-rating', '-recommendation_date')[:limit]

    def get_recommendations_stats(self) -> Dict[str, Any]:
        """
        Get statistics about recommendations.
        
        Returns:
            Dictionary with recommendation statistics
        """
        public_recommendations = self.get_public_recommendations()
        
        return {
            'total_recommendations': public_recommendations.count(),
            'featured_recommendations': public_recommendations.filter(is_featured=True).count(),
            'average_rating': public_recommendations.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
            'rating_distribution': {
                '5_stars': public_recommendations.filter(rating=5).count(),
                '4_stars': public_recommendations.filter(rating=4).count(),
                '3_stars': public_recommendations.filter(rating=3).count(),
                '2_stars': public_recommendations.filter(rating=2).count(),
                '1_star': public_recommendations.filter(rating=1).count(),
            },
            'companies_count': public_recommendations.values('recommender_company').distinct().count(),
            'latest_recommendation_date': public_recommendations.order_by('-recommendation_date').first().recommendation_date if public_recommendations.exists() else None
        }

    def get_recommendations_by_relationship(self, relationship_type: str) -> QuerySet:
        """
        Get recommendations by relationship type.
        
        Args:
            relationship_type: Type of professional relationship
            
        Returns:
            QuerySet of recommendations from that relationship type
        """
        return self.filter_by(
            is_public=True,
            relationship__icontains=relationship_type
        )

    def get_companies_list(self) -> List[str]:
        """
        Get list of unique companies that provided recommendations.
        
        Returns:
            List of company names
        """
        return list(
            self.get_public_recommendations()
            .values_list('recommender_company', flat=True)
            .distinct()
            .order_by('recommender_company')
        )

    def get_skills_list(self) -> List[str]:
        """
        Get list of all skills mentioned in recommendations.
        
        Returns:
            List of unique skills
        """
        skills_set = set()
        recommendations = self.get_public_recommendations().exclude(skills_mentioned=[])
        
        for recommendation in recommendations:
            if isinstance(recommendation.skills_mentioned, list):
                skills_set.update(recommendation.skills_mentioned)
        
        return sorted(list(skills_set))

    def toggle_featured_status(self, recommendation_id: str) -> Recommendation:
        """
        Toggle the featured status of a recommendation.
        
        Args:
            recommendation_id: ID of the recommendation
            
        Returns:
            Updated recommendation instance
        """
        recommendation = self.get_by_id(recommendation_id)
        recommendation.is_featured = not recommendation.is_featured
        recommendation.save(update_fields=['is_featured'])
        return recommendation

    def update_display_order(self, recommendations_order: List[Dict[str, Any]]) -> bool:
        """
        Update display order for multiple recommendations.
        
        Args:
            recommendations_order: List of dicts with 'id' and 'order' keys
            
        Returns:
            True if updated successfully
        """
        recommendations_to_update = []
        
        for item in recommendations_order:
            recommendation = self.get_by_id(item['id'])
            recommendation.display_order = item['order']
            recommendations_to_update.append(recommendation)
        
        self.bulk_update(recommendations_to_update, ['display_order'])
        return True
