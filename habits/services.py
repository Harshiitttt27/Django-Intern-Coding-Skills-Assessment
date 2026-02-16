from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from .models import Habit


def habits_completed_5_times_last_7_days():
    """
    Fetch habits completed at least 5 times in last 7 days.
    Uses ORM only.
    """

    seven_days_ago = timezone.now().date() - timedelta(days=7)

    return (
        Habit.objects
        .filter(is_active=True)
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
    )
