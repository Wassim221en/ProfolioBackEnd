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