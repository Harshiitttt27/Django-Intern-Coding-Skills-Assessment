## Django Intern Coding Assessment – Habit Tracker

----------------------------------------------

## PART 1 – Model Design

Created:
- Habit model
- HabitLog model

Constraints:
- unique_together on (user, name) prevents duplicate habits per user.
- UniqueConstraint on (habit, date) prevents duplicate logs per day.

do NOT store:
- streak
- total completions
- weekly stats

These are derived values and calculated dynamically.

----------------------------------------------

## PART 2 – Prevent Inactive Habit Logging

override clean() in HabitLog.
If habit.is_active is False, log creation raises ValidationError.

----------------------------------------------

## PART 3 – ORM Query

Use annotate + Count with filter argument to fetch habits
completed at least 5 times in last 7 days.

No raw SQL used.

----------------------------------------------

## PART 4 – Debugging Risks

Possible risks in naive view:

## 1. No ownership check
If i  fetch Habit using only id, a user may create logs for another user's habit.
Solution: Always filter by user=request.user

## 2. No duplicate handling.
Without proper handling, multiple requests can create duplicate logs for the same habit on the same day.
Solution: Use a database-level UniqueConstraint on (habit, date).

## 3. No inactive habit validation.
Logs may be created even if the habit is inactive.
Solution: Validation is enforced in the model using clean() method.

----------------------------------------------

## PART 5 – Streak Logic

Streak is calculated dynamically by checking consecutive
completed days from today backwards.

- Dynamic calculation avoids data inconsistency.
- Storing streak improves performance but risks corruption.

----------------------------------------------

## Working Flow 
```
User creates habit
↓
Habit saved with unique name per user
↓
User logs daily
↓
clean() ensures habit active
↓
UniqueConstraint ensures one log per day
↓
Manager fetches filtered habits
↓
Streak calculated dynamically
```

## Project Structure
```
habit_tracker/
    habit_tracker/
        settings.py
    habits/
        models.py
        utils.py
        services.py
        admin.py
    manage.py
    README.md
```
## Working of each file in project , what they actually do??
> settings.py

Contains All the project configurations

> models.py 

Contains core database models and business logic.

> utils.py 

Contains helper functions that are not stored in the database.

> services.py

Contains reusable ORM query logic.

> admin.py

Register models in django admin pannel

> manage.py 

Django’s command-line utility, Used for: Running server, Running migrations, Creating superuser, Managing project commands