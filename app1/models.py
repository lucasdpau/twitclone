from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   #it's best to import settings to reference the builtin user model
    
    def __str__(self): #instead of printing [object at asdasd], this lets python know what to print
        return f"{self.text} at {self.datetime} by {self.author}"