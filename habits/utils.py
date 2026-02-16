from datetime import timedelta
from django.utils import timezone


def calculate_streak(habit): ## Function to calculate current streak for a habit.
    """
    Calculates current streak dynamically.
    We do NOT store streak in DB because it is derived data.
    """

    logs = habit.logs.filter(completed=True).order_by('-date') ## Get completed logs for the habit, ordered by date descending (most recent first).
    today = timezone.now().date() ## Get today's date.

    streak = 0 ## Initialize streak count to 0.

    for log in logs: ## Iterate through the logs to calculate the streak.
        if log.date == today - timedelta(days=streak): ## Check if the log date matches the expected date for the current streak count.
            streak += 1 ## If it matches, increment the streak count and continue checking the next log.
        else: ## If it doesn't match, it means the streak is broken
            break

    return streak ## Return the calculated streak count.
