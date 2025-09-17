from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Manager that excludes soft deleted objects by default.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self):
        """Return queryset including soft deleted objects."""
        return super().get_queryset()

    def deleted_only(self):
        """Return only soft deleted objects."""
        return super().get_queryset().filter(is_deleted=True)


class TimestampedManager(models.Manager):
    """
    Manager with utility methods for timestamp-based queries.
    """
    def created_today(self):
        """Return objects created today."""
        today = timezone.now().date()
        return self.filter(created_at__date=today)

    def created_this_week(self):
        """Return objects created this week."""
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return self.filter(created_at__gte=week_ago)

    def created_this_month(self):
        """Return objects created this month."""
        month_ago = timezone.now() - timezone.timedelta(days=30)
        return self.filter(created_at__gte=month_ago)

    def updated_recently(self, hours=24):
        """Return objects updated within the specified hours."""
        cutoff = timezone.now() - timezone.timedelta(hours=hours)
        return self.filter(updated_at__gte=cutoff)


class BaseManager(SoftDeleteManager, TimestampedManager):
    """
    Combined manager with soft delete and timestamp functionality.
    """
    pass
