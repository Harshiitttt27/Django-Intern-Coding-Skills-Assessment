from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from .models import Habit


def habits_completed_5_times_last_7_days(): ## Service function to fetch habits completed at least 5 times in last 7 days using ORM only.
    """
    Fetch habits completed at least 5 times in last 7 days.
    Uses ORM only.
    """

    seven_days_ago = timezone.now().date() - timedelta(days=7) ## Calculate the date 7 days ago from today.

    return (
        Habit.objects
        .filter(is_active=True) ## Filter active habits
        .annotate(
            recent_count=Count(
                'logs',
                filter=Q( 
                    logs__date__gte=seven_days_ago,
                    logs__completed=True
                )
            )
        )
        .filter(recent_count__gte=5)
    ) ## Filter active habits, annotate with count of completed logs in last 7 days, and filter those with count >= 5.
