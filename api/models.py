from datetime import date
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from datetime import date
class CustomUser(AbstractUser):
    act_choices =    (
        ("sedentary","sedentary"),
        ("light" , "light"),
        ("moderate","moderate"),
        ("high","high"),
        ("extreme","extreme")
    )
    gender_choice = (
        ("male","male"),
        ("female","female")
    )
    # SEDENTARY = 1.2
    # LIGHTLY_ACTIVE = 1.375
    # MODERATELY_ACTIVE = 1.55
    # VERY_ACTIVE = 1.725
    # EXTREMELY_ACTIVE = 1.9
    height = models.FloatField(null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length = 10 , choices = gender_choice, blank=False,null = False)
    activity_factor = models.CharField(max_length = 15 ,choices = act_choices , null = False , blank = False)
    activity_value = models.FloatField(null = True)
    calories = models.IntegerField(null = True)

    REQUIRED_FIELDS =  ["height","weight","age","gender" ,"activity_factor"]
    def save(self , *args , **kwargs):
        if self.activity_factor is None or self.activity_factor == "sedentary" :
            self.activity_value = 1.2
            super().save(*args , **kwargs)
            return
        if self.activity_factor == "light" :
            self.activity_value = 1.375
        elif self.activity_factor == "moderate":
            self.activity_value = 1.55
        elif self.activity_factor == "high" :
            self.activity_value = 1.725
        else :
            self.activity_value = 1.9
        print(self.activity_factor)
        print(self.activity_value)
        if self.gender == "male":
            self.calories = self.activity_value * (88.362 + (13.397*self.weight) + (4.8*self.height) - (5.677*self.age) )
        else :
            self.calories = self.activity_value * (447.593 + (9.247 * self.weight)+ (3.098 *self.height) -(4.33*self.age) )
        print(self.calories)

        super().save(*args , **kwargs)


class DailyCalories(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    consumed_calories = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    def save(self , *args , **kwargs) :
        if self.date is None :
            self.date = date.today()
            print(self.date)
        super().save(*args , **kwargs)
