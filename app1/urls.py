from django.urls import path
from . import views

#url patterns is just a list of all urls supported by the app
#name can be used in the html rendering. eg: a href="{% url 'index' %}"

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("settings", views.settings_view, name="settings"),
    path("profile/<profile_name>", views.profile_view, name="profile"),
    path("reply/<int:tweet_id>", views.reply_view, name="reply",),
    #if the user types an integer into the url, it will go to views.tweet and act appropriately depending on the int
    path("tweets/<int:tweet_id>", views.tweet_view, name="integer"), 
    path("delete/<int:tweet_id>", views.delete_tweet, name="delete"),          
    ] 