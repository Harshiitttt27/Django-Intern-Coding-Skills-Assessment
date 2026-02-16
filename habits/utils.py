from datetime import timedelta
from django.utils import timezone


def calculate_streak(habit):
    """
    Calculates current streak dynamically.
    We do NOT store streak in DB because it is derived data.
    """

    logs = habit.logs.filter(completed=True).order_by('-date')
    today = timezone.now().date()

    streak = 0

    for log in logs:
        if log.date == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return streak
