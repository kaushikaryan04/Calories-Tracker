from django.urls import path
from .views import RegisterUser , DailyCaloriesTrack, CalorieRecord , GenerateReport , GenerateCSVReport
urlpatterns = [
    path("register" , RegisterUser.as_view()),
    path("dailytrack" , DailyCaloriesTrack.as_view()),
    path("getrecord" , CalorieRecord.as_view()),
    path("generatereport" , GenerateReport.as_view()),
    path("generatecsv" , GenerateCSVReport.as_view())
]
