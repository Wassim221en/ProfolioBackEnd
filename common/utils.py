import os
import uuid
from typing import Any, Dict, List, Optional
from django.core.files.storage import default_storage
from django.utils.text import slugify
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def generate_unique_filename(filename: str, prefix: str = "") -> str:
    """
    Generate a unique filename using UUID.
    
    Args:
        filename: Original filename
        prefix: Optional prefix for the filename
        
    Returns:
        Unique filename with original extension
    """
    name, ext = os.path.splitext(filename)
    unique_name = f"{prefix}{uuid.uuid4().hex}{ext}"
    return unique_name


def upload_to_directory(instance, filename: str, directory: str) -> str:
    """
    Generate upload path for file fields.
    
    Args:
        instance: Model instance
        filename: Original filename
        directory: Target directory
        
    Returns:
        Upload path
    """
    unique_filename = generate_unique_filename(filename)
    return os.path.join(directory, unique_filename)


def create_slug(text: str, max_length: int = 50) -> str:
    """
    Create a URL-friendly slug from text.
    
    Args:
        text: Text to convert to slug
        max_length: Maximum length of the slug
        
    Returns:
        URL-friendly slug
    """
    return slugify(text)[:max_length]


def safe_delete_file(file_path: str) -> bool:
    """
    Safely delete a file from storage.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            logger.info(f"File deleted successfully: {file_path}")
            return True
        else:
            logger.warning(f"File not found for deletion: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False


def paginate_queryset(queryset, page_size: int = 20, page: int = 1) -> Dict[str, Any]:
    """
    Manually paginate a queryset.
    
    Args:
        queryset: Django queryset
        page_size: Number of items per page
        page: Page number (1-based)
        
    Returns:
        Dictionary with pagination info
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    paginator = Paginator(queryset, page_size)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return {
        'results': list(page_obj),
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
    }


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def validate_image_file(file) -> bool:
    """
    Validate if uploaded file is a valid image.
    
    Args:
        file: Uploaded file object
        
    Returns:
        True if valid image, False otherwise
    """
    try:
        from PIL import Image
        image = Image.open(file)
        image.verify()
        return True
    except Exception:
        return False


class ResponseFormatter:
    """
    Utility class for formatting API responses consistently.
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
        """Format success response."""
        return {
            'success': True,
            'message': message,
            'data': data,
            'status_code': status_code
        }
    
    @staticmethod
    def error(message: str = "Error", code: str = "error", status_code: int = 400, details: Any = None) -> Dict[str, Any]:
        """Format error response."""
        return {
            'success': False,
            'error': {
                'message': message,
                'code': code,
                'status_code': status_code,
                'details': details
            }
        }
    
    @staticmethod
    def paginated(data: List[Any], pagination_info: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
        """Format paginated response."""
        return {
            'success': True,
            'message': message,
            'data': data,
            'pagination': pagination_info
        }
