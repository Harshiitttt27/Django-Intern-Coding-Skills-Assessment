from django.contrib import admin

# Register your models here.

from .models import Habit, HabitLog

admin.site.register(Habit)
admin.site.register(HabitLog)
