from rest_framework import serializers
from django.utils import timezone


class TimestampedSerializer(serializers.ModelSerializer):
    """
    Base serializer that includes timestamp fields with proper formatting.
    """
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        abstract = True


class BaseModelSerializer(TimestampedSerializer):
    """
    Base serializer for models that inherit from BaseModel.
    """
    id = serializers.UUIDField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        abstract = True


class RatingSerializer(serializers.Serializer):
    """
    Serializer for rating fields with validation.
    """
    rating = serializers.IntegerField(min_value=1, max_value=5)
    rating_display = serializers.SerializerMethodField()

    def get_rating_display(self, obj):
        """Return rating as stars."""
        if hasattr(obj, 'get_rating_display'):
            return obj.get_rating_display()
        rating = getattr(obj, 'rating', 0)
        return "★" * rating + "☆" * (5 - rating)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FileUploadSerializer(serializers.Serializer):
    """
    Serializer for file upload operations.
    """
    file = serializers.FileField()
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_file(self, value):
        """Validate file size and type."""
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        return value


class ImageUploadSerializer(FileUploadSerializer):
    """
    Serializer for image upload operations with additional validation.
    """
    
    def validate_file(self, value):
        """Validate image file."""
        value = super().validate_file(value)
        
        # Check if it's an image
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File must be an image.")
        
        # Additional image validation can be added here
        from common.utils import validate_image_file
        if not validate_image_file(value):
            raise serializers.ValidationError("Invalid image file.")
        
        return value
