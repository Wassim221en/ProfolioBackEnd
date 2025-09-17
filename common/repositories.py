from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import NotFoundError, ValidationError


class BaseRepository(ABC):
    """
    Abstract base repository class that defines the interface for data access.
    """
    
    def __init__(self, model: models.Model):
        self.model = model

    @abstractmethod
    def get_all(self, **filters) -> QuerySet:
        """Get all objects with optional filters."""
        pass

    @abstractmethod
    def get_by_id(self, obj_id: Union[int, str]) -> models.Model:
        """Get object by ID."""
        pass

    @abstractmethod
    def create(self, **data) -> models.Model:
        """Create a new object."""
        pass

    @abstractmethod
    def update(self, obj_id: Union[int, str], **data) -> models.Model:
        """Update an existing object."""
        pass

    @abstractmethod
    def delete(self, obj_id: Union[int, str]) -> bool:
        """Delete an object."""
        pass


class DjangoRepository(BaseRepository):
    """
    Concrete implementation of BaseRepository for Django models.
    """

    def get_all(self, **filters) -> QuerySet:
        """
        Get all objects with optional filters.
        
        Args:
            **filters: Django ORM filters
            
        Returns:
            QuerySet of objects
        """
        return self.model.objects.filter(**filters)

    def get_by_id(self, obj_id: Union[int, str]) -> models.Model:
        """
        Get object by ID.
        
        Args:
            obj_id: Object ID
            
        Returns:
            Model instance
            
        Raises:
            NotFoundError: If object not found
        """
        try:
            return self.model.objects.get(id=obj_id)
        except ObjectDoesNotExist:
            raise NotFoundError(f"{self.model.__name__} with id {obj_id} not found")

    def get_by_field(self, field_name: str, value: Any) -> models.Model:
        """
        Get object by a specific field.
        
        Args:
            field_name: Name of the field
            value: Value to search for
            
        Returns:
            Model instance
            
        Raises:
            NotFoundError: If object not found
        """
        try:
            return self.model.objects.get(**{field_name: value})
        except ObjectDoesNotExist:
            raise NotFoundError(f"{self.model.__name__} with {field_name}={value} not found")

    def filter_by(self, **filters) -> QuerySet:
        """
        Filter objects by multiple criteria.
        
        Args:
            **filters: Django ORM filters
            
        Returns:
            QuerySet of filtered objects
        """
        return self.model.objects.filter(**filters)

    def create(self, **data) -> models.Model:
        """
        Create a new object.
        
        Args:
            **data: Object data
            
        Returns:
            Created model instance
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            obj = self.model(**data)
            obj.full_clean()  # Validate the model
            obj.save()
            return obj
        except Exception as e:
            raise ValidationError(f"Failed to create {self.model.__name__}: {str(e)}")

    def update(self, obj_id: Union[int, str], **data) -> models.Model:
        """
        Update an existing object.
        
        Args:
            obj_id: Object ID
            **data: Updated data
            
        Returns:
            Updated model instance
            
        Raises:
            NotFoundError: If object not found
            ValidationError: If data is invalid
        """
        try:
            obj = self.get_by_id(obj_id)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.full_clean()  # Validate the model
            obj.save()
            return obj
        except NotFoundError:
            raise
        except Exception as e:
            raise ValidationError(f"Failed to update {self.model.__name__}: {str(e)}")

    def delete(self, obj_id: Union[int, str]) -> bool:
        """
        Delete an object.
        
        Args:
            obj_id: Object ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundError: If object not found
        """
        obj = self.get_by_id(obj_id)
        obj.delete()
        return True

    def soft_delete(self, obj_id: Union[int, str]) -> bool:
        """
        Soft delete an object (if model supports it).
        
        Args:
            obj_id: Object ID
            
        Returns:
            True if soft deleted successfully
            
        Raises:
            NotFoundError: If object not found
        """
        obj = self.get_by_id(obj_id)
        if hasattr(obj, 'soft_delete'):
            obj.soft_delete()
            return True
        else:
            # Fallback to hard delete
            return self.delete(obj_id)

    def exists(self, **filters) -> bool:
        """
        Check if objects exist with given filters.
        
        Args:
            **filters: Django ORM filters
            
        Returns:
            True if objects exist
        """
        return self.model.objects.filter(**filters).exists()

    def count(self, **filters) -> int:
        """
        Count objects with given filters.
        
        Args:
            **filters: Django ORM filters
            
        Returns:
            Number of objects
        """
        return self.model.objects.filter(**filters).count()

    def get_or_create(self, defaults: Optional[Dict] = None, **kwargs) -> tuple:
        """
        Get or create an object.
        
        Args:
            defaults: Default values for creation
            **kwargs: Lookup parameters
            
        Returns:
            Tuple of (object, created)
        """
        return self.model.objects.get_or_create(defaults=defaults, **kwargs)

    def bulk_create(self, objects_data: List[Dict]) -> List[models.Model]:
        """
        Create multiple objects in bulk.
        
        Args:
            objects_data: List of object data dictionaries
            
        Returns:
            List of created objects
        """
        objects = [self.model(**data) for data in objects_data]
        return self.model.objects.bulk_create(objects)

    def bulk_update(self, objects: List[models.Model], fields: List[str]) -> None:
        """
        Update multiple objects in bulk.
        
        Args:
            objects: List of model instances to update
            fields: List of field names to update
        """
        self.model.objects.bulk_update(objects, fields)
