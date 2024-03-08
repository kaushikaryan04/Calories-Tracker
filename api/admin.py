from django.contrib import admin
from .models import CustomUser, DailyCalories

admin.site.register(CustomUser )
admin.site.register(DailyCalories)
