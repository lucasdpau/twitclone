from django.db import models
from django.utils import timezone

# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=timezone.now)
    
    def __str__(self): #instead of printing [object at asdasd], this lets python know what to print
        return f"{self.text} at {self.datetime}"