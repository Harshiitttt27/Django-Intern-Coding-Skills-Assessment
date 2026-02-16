from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class HabitManager(models.Manager):
    """
    Custom manager to fetch active habits
    with logs in last 7 days.
    """

    def active_with_recent_logs(self):
        from datetime import timedelta

        seven_days_ago = timezone.now().date() - timedelta(days=7)

        return (
            self.get_queryset()
            .filter(is_active=True, logs__date__gte=seven_days_ago)
            .distinct()
        )


class Habit(models.Model):
    """
    Represents a daily habit created by a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits"
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    objects = HabitManager()

    class Meta:
        # Prevent same habit name for same user
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class HabitLog(models.Model):
    """
    Stores daily log for a habit.
    Only one log per habit per day.
    """

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    date = models.DateField(default=timezone.now)

    completed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        constraints = [
            models.UniqueConstraint(
                fields=['habit', 'date'],
                name='one_log_per_day'
            )
        ]

    def clean(self):
        """
        Prevent log creation for inactive habits.
        """
        if not self.habit.is_active:
            raise ValidationError("Cannot log an inactive habit.")

    def save(self, *args, **kwargs):
        
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
