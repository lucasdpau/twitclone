from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User #import the uder model so t hat we can extend it with UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   #it's best to import settings to reference the builtin user model
    parent_tweet = models.IntegerField(null=True)  #None if this is an inital tweet. If you reply to a tweet, the post being replied to is the parent
    
    def __str__(self): #instead of printing [object at asdasd], this lets python know what to print
        return f"Tweet {self.id} {self.text} at {self.datetime} by {self.author} parent {self.parent_tweet}"

#class Follows(models.Model):
    #followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #extend the builtin User model with onetoone
    bio = models.CharField(max_length=300, default="I haven't written a bio yet!")
    profile_pic = models.CharField(max_length=140, default="green_square.jpg")
    location = models.CharField(max_length=60, default="Nowhere")
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    