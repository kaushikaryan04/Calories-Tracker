from rest_framework import serializers
from .models import DailyCalories

class CalorieRecordSerializer(serializers.ModelSerializer) :
    class Meta :
        model = DailyCalories
        fields = ["date" , "consumed_calories"]
