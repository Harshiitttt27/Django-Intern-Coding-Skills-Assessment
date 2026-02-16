from django.contrib import admin

# Register your models here.

from .models import Habit, HabitLog

admin.site.register(Habit) ## Register the Habit model to make it accessible in the Django admin interface.
admin.site.register(HabitLog) ## Register the HabitLog model to make it accessible in the Django admin interface.
