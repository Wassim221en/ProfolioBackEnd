from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from django.db import transaction
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base service class that defines the interface for business logic operations.
    """
    
    def __init__(self, repository):
        self.repository = repository

    @abstractmethod
    def get_all(self, **filters) -> List[Any]:
        """Get all objects with optional filters."""
        pass

    @abstractmethod
    def get_by_id(self, obj_id: Union[int, str]) -> Any:
        """Get object by ID."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        """Create a new object."""
        pass

    @abstractmethod
    def update(self, obj_id: Union[int, str], data: Dict[str, Any]) -> Any:
        """Update an existing object."""
        pass

    @abstractmethod
    def delete(self, obj_id: Union[int, str]) -> bool:
        """Delete an object."""
        pass


class CacheableService:
    """
    Mixin class that provides caching functionality for services.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_timeout = getattr(settings, 'DEFAULT_CACHE_TIMEOUT', 300)  # 5 minutes default

    def get_cache_key(self, key_suffix: str) -> str:
        """
        Generate cache key for the service.
        
        Args:
            key_suffix: Suffix to append to the cache key
            
        Returns:
            Full cache key
        """
        service_name = self.__class__.__name__.lower()
        return f"{service_name}:{key_suffix}"

    def get_from_cache(self, key_suffix: str) -> Any:
        """
        Get data from cache.
        
        Args:
            key_suffix: Cache key suffix
            
        Returns:
            Cached data or None
        """
        cache_key = self.get_cache_key(key_suffix)
        return cache.get(cache_key)

    def set_cache(self, key_suffix: str, data: Any, timeout: Optional[int] = None) -> None:
        """
        Set data in cache.
        
        Args:
            key_suffix: Cache key suffix
            data: Data to cache
            timeout: Cache timeout in seconds
        """
        cache_key = self.get_cache_key(key_suffix)
        cache_timeout = timeout or self.cache_timeout
        cache.set(cache_key, data, cache_timeout)

    def delete_cache(self, key_suffix: str) -> None:
        """
        Delete data from cache.
        
        Args:
            key_suffix: Cache key suffix
        """
        cache_key = self.get_cache_key(key_suffix)
        cache.delete(cache_key)

    def clear_related_cache(self, patterns: List[str]) -> None:
        """
        Clear cache entries matching patterns.
        
        Args:
            patterns: List of cache key patterns to clear
        """
        for pattern in patterns:
            cache_key = self.get_cache_key(pattern)
            cache.delete(cache_key)


class TransactionalService:
    """
    Mixin class that provides transaction management for services.
    """

    def execute_in_transaction(self, func, *args, **kwargs):
        """
        Execute a function within a database transaction.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Transaction failed in {self.__class__.__name__}: {str(e)}")
            raise

    def bulk_operation(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """
        Execute multiple operations in a single transaction.
        
        Args:
            operations: List of operation dictionaries with 'method' and 'args' keys
            
        Returns:
            List of operation results
        """
        def execute_operations():
            results = []
            for operation in operations:
                method = getattr(self, operation['method'])
                args = operation.get('args', [])
                kwargs = operation.get('kwargs', {})
                result = method(*args, **kwargs)
                results.append(result)
            return results

        return self.execute_in_transaction(execute_operations)


class LoggingService:
    """
    Mixin class that provides logging functionality for services.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)

    def log_operation(self, operation: str, obj_id: Optional[Union[int, str]] = None, 
                     extra_data: Optional[Dict] = None) -> None:
        """
        Log service operation.
        
        Args:
            operation: Operation name
            obj_id: Object ID if applicable
            extra_data: Additional data to log
        """
        log_data = {
            'service': self.__class__.__name__,
            'operation': operation,
            'object_id': obj_id,
        }
        if extra_data:
            log_data.update(extra_data)
        
        self.logger.info(f"Service operation: {operation}", extra=log_data)

    def log_error(self, operation: str, error: Exception, obj_id: Optional[Union[int, str]] = None) -> None:
        """
        Log service error.
        
        Args:
            operation: Operation name
            error: Exception that occurred
            obj_id: Object ID if applicable
        """
        log_data = {
            'service': self.__class__.__name__,
            'operation': operation,
            'object_id': obj_id,
            'error': str(error),
        }
        
        self.logger.error(f"Service error in {operation}: {str(error)}", extra=log_data, exc_info=True)


class ValidationService:
    """
    Mixin class that provides validation functionality for services.
    """

    def validate_data(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """
        Validate that required fields are present in data.
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            
        Raises:
            ValidationError: If validation fails
        """
        from common.exceptions import ValidationError
        
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    def validate_business_rules(self, data: Dict[str, Any]) -> None:
        """
        Validate business rules. Override in subclasses.
        
        Args:
            data: Data to validate
            
        Raises:
            BusinessLogicError: If business rules are violated
        """
        pass


class DjangoService(BaseService, CacheableService, TransactionalService, LoggingService, ValidationService):
    """
    Concrete implementation of BaseService for Django applications with additional mixins.
    """

    def get_all(self, use_cache: bool = True, **filters) -> List[Any]:
        """
        Get all objects with optional caching.
        
        Args:
            use_cache: Whether to use caching
            **filters: Filters to apply
            
        Returns:
            List of objects
        """
        cache_key = f"all:{hash(str(sorted(filters.items())))}"
        
        if use_cache:
            cached_data = self.get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data

        try:
            objects = list(self.repository.get_all(**filters))
            
            if use_cache:
                self.set_cache(cache_key, objects)
            
            self.log_operation('get_all', extra_data={'filters': filters, 'count': len(objects)})
            return objects
            
        except Exception as e:
            self.log_error('get_all', e)
            raise

    def get_by_id(self, obj_id: Union[int, str], use_cache: bool = True) -> Any:
        """
        Get object by ID with optional caching.
        
        Args:
            obj_id: Object ID
            use_cache: Whether to use caching
            
        Returns:
            Object instance
        """
        cache_key = f"by_id:{obj_id}"
        
        if use_cache:
            cached_data = self.get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data

        try:
            obj = self.repository.get_by_id(obj_id)
            
            if use_cache:
                self.set_cache(cache_key, obj)
            
            self.log_operation('get_by_id', obj_id)
            return obj
            
        except Exception as e:
            self.log_error('get_by_id', e, obj_id)
            raise

    def create(self, data: Dict[str, Any]) -> Any:
        """
        Create a new object with validation and logging.
        
        Args:
            data: Object data
            
        Returns:
            Created object
        """
        try:
            self.validate_business_rules(data)
            
            def create_operation():
                obj = self.repository.create(**data)
                self.clear_related_cache(['all'])  # Clear list caches
                return obj
            
            obj = self.execute_in_transaction(create_operation)
            self.log_operation('create', obj.id if hasattr(obj, 'id') else None)
            return obj
            
        except Exception as e:
            self.log_error('create', e)
            raise

    def update(self, obj_id: Union[int, str], data: Dict[str, Any]) -> Any:
        """
        Update an existing object with validation and logging.
        
        Args:
            obj_id: Object ID
            data: Updated data
            
        Returns:
            Updated object
        """
        try:
            self.validate_business_rules(data)
            
            def update_operation():
                obj = self.repository.update(obj_id, **data)
                self.delete_cache(f"by_id:{obj_id}")  # Clear object cache
                self.clear_related_cache(['all'])  # Clear list caches
                return obj
            
            obj = self.execute_in_transaction(update_operation)
            self.log_operation('update', obj_id)
            return obj
            
        except Exception as e:
            self.log_error('update', e, obj_id)
            raise

    def delete(self, obj_id: Union[int, str]) -> bool:
        """
        Delete an object with logging.
        
        Args:
            obj_id: Object ID
            
        Returns:
            True if deleted successfully
        """
        try:
            def delete_operation():
                result = self.repository.delete(obj_id)
                self.delete_cache(f"by_id:{obj_id}")  # Clear object cache
                self.clear_related_cache(['all'])  # Clear list caches
                return result
            
            result = self.execute_in_transaction(delete_operation)
            self.log_operation('delete', obj_id)
            return result
            
        except Exception as e:
            self.log_error('delete', e, obj_id)
            raise
