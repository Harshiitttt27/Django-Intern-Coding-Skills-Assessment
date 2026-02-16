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

    def active_with_recent_logs(self): ## method to fetch active habits with logs in last 7 days
        from datetime import timedelta

        seven_days_ago = timezone.now().date() - timedelta(days=7)

        return (
            self.get_queryset()
            .filter(is_active=True, logs__date__gte=seven_days_ago)
            .distinct()
        ) ## distinct() to avoid duplicates if multiple logs in last 7 days


class Habit(models.Model):
    """
    Represents a daily habit created by a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits"
    ) 
    ## Each habit is linked to a user, and if the user is deleted, their habits are also deleted
     ## CASCADE ensures habits are deleted if user is deleted.
    ## related_name allows reverse access: user.habits.all()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True) ## Indicates if the habit is currently active. Inactive habits cannot be logged.

    created_at = models.DateTimeField(auto_now_add=True) ## Automatically set when habit is created

    
    objects = HabitManager() ## Use custom manager for additional query methods

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
    ## Each log is linked to a habit, and if the habit is deleted, its logs are also deleted
     ## CASCADE ensures logs are deleted if habit is deleted.
     ## related_name allows reverse access: habit.logs.all()

    date = models.DateField(default=timezone.now) ## Date of the log, defaults to today

    completed = models.BooleanField(default=True) ## Indicates if the habit was completed on that day. 

    created_at = models.DateTimeField(auto_now_add=True) ## Automatically set when log is created

    class Meta:
        
        constraints = [
            models.UniqueConstraint(
                fields=['habit', 'date'],
                name='one_log_per_day'
            )
        ]
     ## Ensures that there can only be one log per habit per day, preventing duplicates.

    def clean(self): ##  clean method to add custom validation logic
        """
        Prevent log creation for inactive habits.
        """
        if not self.habit.is_active:
            raise ValidationError("Cannot log an inactive habit.")

    def save(self, *args, **kwargs): ## Override save to call full_clean before saving, ensuring validation is enforced.
        
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self): ## String representation of the log, showing habit name and date.
        return f"{self.habit.name} - {self.date}"
