from django.contrib.auth import authenticate, login, logout #import djangos builtin authentication library
from django.contrib.auth.models import User              #Allows us to create users and save to the DB
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Tweet
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {}) #renders from the templates folder in the app folder
    current_username = request.user.username
    users = User.objects.filter(username="lucas")    
    context = {"tweets": Tweet.objects.all(), "users":users, "current_username":current_username}
    authenticated_username = request.user.username
    return render(request, "index.html", context)

def login_view(request):  #if we name this function 'login', it will be the same as the imported login function so it won't work.
    #If a HTTP POST request is made
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) #Django has built in logout and login functions, so we dont have to code it manually like in flask
            return HttpResponseRedirect(reverse("index"))  # reverses the urlname back to url, so that from the name index we get the url.
        
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})
    #Else if a HTTP GET request is made
    else:
        return render(request, "login.html")
    
def logout_view(request):
    #Django has built in logout and login functions, so we dont have to code it manually like in flask
    logout(request)
    return render(request, "login.html", {"message":"Logged out."})
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        if len(username) == 0:
            return render(request, "register.html", {"message": "Please enter a username"})
        elif len(email) == 0:
            return render(request, "register.html", {"message": "Please enter an email"})
        elif len(password) == 0:
            return render(request, "register.html", {"message": "Please enter a password"})
        elif len(confirm) == 0:
            return render(request, "register.html", {"message": "Please confirm the password"})
        
        if password == confirm:
            #TODO avoid duplicate usernames
            user = User.objects.create_user(username, email, password)
            user.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"message": "Passwords don't match"})
    else:
        return render(request, "register.html")
    
    
def profile_view(request, profile_name):
    if request.method == "POST":  #if a form has been submitted then we add it to the database
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user)
            new_tweet.save()
    profile_string = profile_name
    current_username = request.user.username
    users = User.objects.filter(username="lucas")
    tweets = Tweet.objects.filter(author__username=profile_string)
    return render(request, "profile.html", {"message": profile_string, "tweets":tweets, "users":users, "current_username":current_username})

def reply_view(request, tweet_id):
    #tweet_id is the int in the url reply/<int:tweet_id>
    parent = tweet_id
    parent_tweet = Tweet.objects.filter(id=tweet_id)[0]
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")
        if len(tweet_text) <= 140:
            new_tweet = Tweet(text=tweet_text, author=request.user, parent_tweet=parent)
            new_tweet.save()
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "reply.html", {"tweet_id": parent, "parent_tweet": parent_tweet})

def tweet_view(request, tweet_id):   # tweet_id from path <int:tweet_id> in urls.py
    return_string = str(tweet_id)
    return render(request, "tweet.html", {}) #this loads a webpage that only contains the int entered in the url