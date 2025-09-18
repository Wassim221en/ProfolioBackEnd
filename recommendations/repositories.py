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
