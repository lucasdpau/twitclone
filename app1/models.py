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
    parent_tweet_obj = models.ForeignKey('Tweet', on_delete=models.CASCADE, null=True)
    replies = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    deleted_text = models.CharField(default="", max_length=200)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self): #instead of printing [object at asdasd], this lets python know what to print
        return f"Tweet {self.id} {self.text} at {self.datetime} by {self.author} parent {self.parent_tweet}"

class Tags(models.Model):
    tagname = models.CharField(max_length=50)
    tweets = models.ManyToManyField(Tweet)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #extend the builtin User model with onetoone
    bio = models.CharField(max_length=300, default="I haven't written a bio yet!")
    profile_pic = models.CharField(max_length=140, default="default-user-image.png")
    location = models.CharField(max_length=60, default="Nowhere")
    fav_tweets = models.ManyToManyField(Tweet, related_name="bookmarked_by")
    liked_tweets = models.ManyToManyField(Tweet, related_name="liked_by")
    retweets = models.ManyToManyField(Tweet, related_name="retweeted_by")
    following = models.ManyToManyField('Profile', related_name='followed_by')
    dark_mode = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_shadow_banned = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    default_page = models.CharField(max_length=20, default="all")
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    